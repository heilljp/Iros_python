import datetime
import hashlib
import json
import os
import time
import traceback
from dataclasses import dataclass, field

import bs4
from PySide6.QtCore import Signal, QThread
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from iros_variables import ThreadState, ThreadkillException, LOG_PATH, BASE_URL, SESSION_PATH, ProcessResult, \
    RESULT_PATH

import iros_functions as rf


@dataclass
class UpdateEvent:
    number: int
    current: int
    total: int
    item_name: str

    success: bool = False


@dataclass
class SendMessageEvent:
    message: str


@dataclass
class FinishEvent:
    state: ThreadState
    error_message: str = field(default="")


class ProcessThread(QThread):
    finishSignal = Signal(ThreadState)
    updateSignal = Signal(UpdateEvent)
    sendMessageSignal = Signal(SendMessageEvent)

    def __init__(self, _id: str, password: str, start: int, end: int, place: str, path: str, hidden: bool = True,
                 append_option: bool = False):
        super().__init__()
        self.kill_requested = False

        self._id = _id
        self.password = password

        self.start_index = int(start)
        self.end_index = end

        self.fixed_start = start
        self.fixed_end = end
        self.length = end - start + 1

        self.place = place

        self.path = path

        self.hidden = hidden
        self.append_option = append_option

        self.drv = None

    def send_message(self, txt):
        self.sendMessageSignal.emit(SendMessageEvent(message=txt))

    def get_order(self, target: int):
        items = list(range(self.fixed_start, self.fixed_end + 1))
        index = None
        if target in items:
            index = items.index(target) + 1
        return index

    def run(self):
        completed = []
        dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fail_list_file = f"실패리스트_{dstring}.txt"
        fail_list_path = f"{RESULT_PATH}/{fail_list_file}"
        os.makedirs(RESULT_PATH, exist_ok=True)
        self.send_message("안녕하세요.")

        state = ThreadState.RUNNING

        try:

            if not self.append_option:
                rf.empty_file(self.path)
            else:
                last_item = rf.get_last_company(self.path)
                last_index = int(last_item.reg_number)
                if last_index >= self.start_index and last_index < self.end_index:
                    self.start_index = last_index + 1

            rf.set_protected_mode(True)

            target = None
            count = 0
            while self.start_index < self.end_index:
                self.kill_check()
                self.drv = rf.make_driver(hidden=self.hidden)
                if not self.login_process(self._id, self.password, self.drv, force=False):
                    continue
                result = self.select_process(self.drv, self.start_index, self.end_index, target_number=target)
                if self.start_index == result.current:
                    count += 1
                    if count > 3:
                        count = 0
                        with open(fail_list_path, "a", encoding="utf-8") as f:
                            f.write(f"{self.place} : {self.start_index}\n")
                        self.start_index += 1
                        continue
                else:
                    count = 0
                self.start_index = result.current
                target = result.target
            state = ThreadState.COMPLETE
        except ThreadkillException:
            state = ThreadState.CANCELLED
            print("취소되었습니다.")
        except Exception:
            state = ThreadState.ERROR
            te = traceback.format_exc()
            print(te)

            dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(LOG_PATH, exist_ok=True)
            file = open(f"{LOG_PATH}/log_{dstring}.txt", "w", encoding="utf-8")
            file.write(te)
            file.close()
        finally:
            self.finishSignal.emit(FinishEvent(state=state))
            if self.drv:
                self.drv.quit()

    def kill(self):
        self.kill_requested = True

    def kill_check(self):
        if self.kill_requested:
            raise ThreadkillException

    def login(self, login_id, login_password, drv: webdriver.Ie):
        drv.get(f"{BASE_URL}/re1/intro.jsp?smsgubun=N&sysid=PL")
        self.kill_check()
        time.sleep(3)
        self.kill_check()
        id_tag = drv.find_element(By.NAME, "user_id")
        password_tag = drv.find_element(By.NAME, "password")

        id_tag.send_keys(login_id)

        password_tag.send_keys(login_password)

        for i in range(5):
            try:
                self.kill_check()
                login_btn = drv.find_element(By.CSS_SELECTOR, "a.btn_log4")
                login_btn.click()
                WebDriverWait(drv, 5).until(EC.url_to_be("http://www.iros.go.kr/PMainJ.jsp"))
                break
            except:
                traceback.print_exc()
                pass
        else:
            raise Exception

        result = []

        for ck in drv.get_cookies():
            c = {
                'name': ck['name'],
                'value': ck['value'],
                'domain': ck['domain'],
            }
            result.append(c)

        return result

    def login_process(self, login_id, login_password, drv: webdriver.Ie, force=False, close_delay=10) -> bool:
        result = True
        try:
            os.makedirs(SESSION_PATH, exist_ok=True)
            md5 = hashlib.md5(login_id.encode()).hexdigest()

            self.kill_check()

            files = os.listdir(SESSION_PATH)
            ds = []
            for file in filter(lambda x: md5 in x and '.txt' in x, files):
                file = file.replace(".txt", "")
                m, d = file.split("_")
                ds.append(d)

            ds.sort()
            selected = ds[-1] if len(ds) > 0 else None
            if selected:
                date_obj = datetime.datetime.strptime(selected, "%Y%m%d%H%M%S")
                delta = datetime.datetime.now() - date_obj
                seconds = delta.seconds
            else:
                seconds = 0

            result = None

            one_hour = 3600

            if seconds > one_hour or force or not selected:
                dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                data = self.login(login_id, login_password, drv)
                with open(f"{SESSION_PATH}/{md5}_{dstring}.txt", "w", encoding="utf-8") as f:
                    f.write(json.dumps(data))
                result = data
            else:
                filename = f"{md5}_{selected}.txt"
                with open(f"{SESSION_PATH}/{filename}", "r", encoding="utf-8") as f:
                    result = json.loads(f.read())

                drv.get(BASE_URL)
                time.sleep(3)
                for ck in result:
                    drv.add_cookie(ck)
                time.sleep(3)
                drv.get(BASE_URL)

            rf.close_windows_except(drv, "인터넷등기소")
        except Exception:
            result = False
            drv.quit()
            time.sleep(close_delay)
        finally:
            return result

    def update(self, number: int, success=False):
        self.updateSignal.emit(UpdateEvent(
            number=number,
            current=self.get_order(number),
            total=self.length,
            item_name='',
            success=success,
        ))

    def select_process(self, drv: webdriver.Ie, start_index, end_index, target_number=None) -> ProcessResult:
        try:
            current = start_index
            self.update(current)
            result = ProcessResult(current=current, target=target_number)
            self.kill_check()

            _wait = WebDriverWait(drv, 15)

            actions = ActionChains(drv)

            drv.get(f'{BASE_URL}/efrontservlet?cmd=EC2GetBfPayListC&work_cls=E')
            self.kill_check()
            for i in range(10):
                self.kill_check()
                if target_number:
                    _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sbtn_bg02_action")))
                    target = _wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{target_number}')]")))
                    target.click()
                else:
                    rf.find_and_click_button_with_text(drv, '신규')
                time.sleep(2)
                if not "/efrontservlet?cmd=EC2GetBfPayListC&work_cls=E" in drv.current_url:
                    break
            else:
                raise Exception
            self.kill_check()
            select_type_tage = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select#id_corp_cls")))
            actions.move_to_element(select_type_tage).pause(3)

            rf.find_select_and_click_option(drv, "select#id_corp_cls", '주식회사')
            rf.find_select_and_click_option(drv, "select#id_rgs_type_cd", '변경등기')

            select_type2_tage = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select#id_rgs_type_cd")))
            actions.move_to_element(select_type2_tage).pause(1)

            while 1:
                self.update(current)
                input_button = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#corpImg2")))
                actions.move_to_element(input_button).pause(1).perform()
                self.kill_check()
                for i in range(10):
                    rf.find_and_click_button(drv, "button#corpImg2")
                    rf.select_window(drv, "대상법인검색(등기번호)", exception=True)
                    time.sleep(2)
                    self.kill_check()
                    if "대상법인검색(등기번호)" in drv.title:
                        break
                else:
                    raise Exception

                rf.find_select_and_click_option_exact(drv, "select#id_regt_no", self.place)

                while 1:
                    self.update(current)

                    rf.find_input_and_set_value(drv, "input#id_dg_no", current)
                    rf.find_and_click_button(drv, "button.sbtn_bg02_action")
                    self.kill_check()
                    check = rf.find_company(drv)
                    if check:
                        rf.find_and_click_button(drv, "button#btn_select")
                        try:
                            WebDriverWait(drv, 5).until(EC.number_of_windows_to_be(3))
                            rf.select_window(drv, "신청사건 계류정보 확인")
                            rf.find_and_click_button_with_text(drv, "확인")
                        except:
                            alert_text = rf.check_if_alert_exists(drv)
                            if alert_text and '해상간주' in alert_text:
                                rf.check_if_alert_exists(drv)

                        number_of_windows: bool = WebDriverWait(drv, 15).until(EC.number_of_windows_to_be(1))
                        if not number_of_windows:
                            raise Exception

                        drv.switch_to.window(drv.window_handles[-1])
                        break
                    if current == end_index:
                        break
                    current += 1
                    result.current = current
                    time.sleep(0)

                if current == end_index:
                    break

                rf.select_window(drv, "신청서작성현황")
                self.kill_check()
                rf.find_select_and_click_option(drv, "select#id_rgs_rsn_cd", '(대표)이사/감사 등의 임원사항 변경')

                rf.find_input_and_send_keys(drv, "textarea#rgs_rsn", "1")

                isoup = bs4.BeautifulSoup(drv.page_source, "html.parser")
                target_tag = isoup.select_one("input[name='enr_recev_no']")
                target_number = target_tag.attrs['value'] if 'value' in target_tag.attrs and target_tag.attrs[
                    'value'] else None
                result.target = target_number

                rf.find_and_click_button(drv, "input#id_chk_form_delete")
                self.kill_check()
                for i in range(10):
                    try:
                        self.kill_check()
                        rf.find_and_click_button(drv, "button#button_next")
                        try:
                            self.kill_check()
                            WebDriverWait(drv, 3).until(EC.number_of_windows_to_be(2))
                            drv.switch_to.window(drv.window_handles[-1])
                            WebDriverWait(drv, 3).until(EC.title_contains("예외사항내역"))
                            self.kill_check()
                            rf.find_and_click_button_with_xpath(drv, "//img[@alt='창닫기']/..")
                            WebDriverWait(drv, 3).until(EC.number_of_windows_to_be(1))
                            drv.switch_to.window(drv.window_handles[-1])
                            self.kill_check()

                        except TimeoutException:
                            pass
                        _wait.until(EC.url_contains("cmd=EC2SaveWriteApplStep1C"))
                        break
                    except:
                        pass
                else:
                    raise Exception

                actions = ActionChains(drv)
                input_button = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#Entry")))

                actions \
                    .move_to_element(input_button).pause(.5).perform()

                for i in range(10):
                    self.kill_check()
                    rf.find_and_click_button(drv, "button#Entry")
                    try:
                        _wait.until(EC.number_of_windows_to_be(2))
                        break
                    except:
                        pass

                rf.select_window(drv, "등기할사항")

                company = rf.get_company_info(drv)
                result.companies.append(company)

                current_handle = drv.current_window_handle
                for i in range(10):
                    self.kill_check()
                    rf.find_and_click_button_with_xpath(drv, "//img[@alt='창닫기']/..")
                    time.sleep(2)
                    if rf.check_if_window_closed(drv, current_handle):
                        break
                else:
                    raise Exception
                rf.select_window(drv, "신청서작성현황")

                if current == end_index:
                    break

                for i in range(3):
                    self.kill_check()
                    rf.find_and_click_button_with_text(drv, '이전')
                    try:
                        WebDriverWait(drv, 10).until(EC.url_contains("cmd=EC2GetWriteApplStep1C"))
                        break
                    except:
                        pass
                else:
                    raise Exception
                rf.save_company(company, self.path)
                self.update(current, success=True)
                current += 1
                result.current = current

        except:
            fe = traceback.format_exc()
            dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(LOG_PATH, exist_ok=True)
            file = open(f"{LOG_PATH}/log_{dstring}.txt", "w", encoding="utf-8")
            file.write(fe)
            file.close()
            for i in range(10):
                try:
                    drv.quit()
                    break
                except:
                    time.sleep(2)
        finally:
            return result
