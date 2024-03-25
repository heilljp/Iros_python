import time
import traceback

import winreg

import bs4
import psutil

from selenium.common import TimeoutException, NoSuchWindowException
from selenium.webdriver import ActionChains

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from iros_variables import *

import edgedriver_autoinstaller

edgedriver_path = edgedriver_autoinstaller.install()


def make_driver(hidden=False) -> webdriver.Ie:
    ieOptions = webdriver.IeOptions()
    ieOptions.attach_to_edge_chrome = True
    ieOptions.add_additional_option("ie.edgechromium", True)

    if hidden:
        ieOptions.add_argument("--headless")
    _driver = webdriver.Ie(
        options=ieOptions,
    )

    return _driver


def find_input_and_send_keys(_drv: webdriver.Ie, css_selector, input_txt, wait_time=15):
    _wait = WebDriverWait(_drv, wait_time)
    input_tag = _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    input_tag.clear()
    input_tag.send_keys(input_txt)


def find_input_and_set_value(_drv: webdriver.Ie, css_selector, input_txt, wait_time=15):
    _wait = WebDriverWait(_drv, wait_time)
    input_tag = _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    _drv.execute_script(f"arguments[0].setAttribute('value', '{input_txt}');", input_tag)


def find_select_and_click_option(_drv: webdriver.Ie, select_css_selector, option_txt, wait_time=15):
    _wait = WebDriverWait(_drv, wait_time)
    select_tag = _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, select_css_selector)))
    target_option = select_tag.find_element(By.XPATH, f"option[contains(text(),'{option_txt}')]")
    target_option.click()


def find_select_and_click_option_exact(_drv: webdriver.Ie, select_css_selector, option_txt, wait_time=15):
    _wait = WebDriverWait(_drv, wait_time)
    select_tag = _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, select_css_selector)))
    options = select_tag.find_elements(By.CSS_SELECTOR, "option")

    select_inner_html = select_tag.get_attribute('innerHTML')
    isoup = bs4.BeautifulSoup(select_inner_html, "html.parser")
    options = isoup.select("option")
    option_length = len(option_txt.split())
    target_option = None
    for opt in options:
        opt_txt = opt.text.strip()
        opt_len = len(opt_txt.split())
        if option_length == opt_len:
            for i in filter(lambda x: x, option_txt.strip().split()):
                if not i in opt_txt:
                    print(i)
                    break
            else:
                target_option = opt
        if target_option:
            break
    value = target_option.attrs['value']
    option: WebElement = select_tag.find_element(By.XPATH, f"option[@value='{value}']")
    _drv.execute_script("arguments[0].setAttribute('selected', 'selected');", option)


def find_and_click_button(_drv: webdriver.Ie, css_selector, wait_time=15, delay=0):
    _wait = WebDriverWait(_drv, wait_time)
    _button = _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    time.sleep(delay)
    _button.click()


def find_and_click_button_with_xpath(_drv: webdriver.Ie, path, wait_time=15, delay=0):
    try:
        _wait = WebDriverWait(_drv, wait_time)
        _button = _wait.until(
            EC.element_to_be_clickable((By.XPATH, path)))
        time.sleep(delay)
        _button.click()
    except NoSuchWindowException:
        return


def find_and_click_button_with_text(_drv: webdriver.Ie, txt, wait_time=15, delay=0):
    _wait = WebDriverWait(_drv, wait_time)
    _button = _wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{txt}')]")))
    time.sleep(delay)
    _button.click()


def close_windows_except(drv: webdriver.Ie, target_title, delay=3):
    close_target_handles = []

    time.sleep(delay)
    back_to = None
    for handle in drv.window_handles:
        drv.switch_to.window(handle)

        if drv.title != target_title:
            close_target_handles.append(handle)
        else:
            back_to = handle
    for handle in close_target_handles:
        drv.switch_to.window(handle)
        drv.close()

    drv.switch_to.window(back_to)


def select_window(_drv: webdriver.Ie, target_title, delay=1, exception=True):
    time.sleep(delay)
    target = None

    for i in range(8):
        for handle in _drv.window_handles:
            _drv.switch_to.window(handle)
            print(handle, _drv.title)
            if _drv.title == target_title:
                target = handle
        if target:
            _drv.switch_to.window(target)
            break
        time.sleep(2)
    else:
        if exception:
            raise Exception


def save_html(_drv: webdriver.Ie, name="", dstring=None):
    if not dstring:
        dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if name:
        name = f"_{name}"
    with open(f"result/page_{dstring}{name}.html", "w", encoding="utf-8") as f:
        f.write(_drv.page_source)


def make_html_for_dev(_drv: webdriver.Ie):
    dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    frame = _drv.find_element(By.CSS_SELECTOR, "iframe")
    _drv.switch_to.frame(frame)

    fid = "entryTopFrame"
    frame = _drv.find_element(By.CSS_SELECTOR, f"iframe#{fid}")
    _drv.switch_to.frame(frame)
    save_html(_drv, name=fid, dstring=dstring)
    _drv.switch_to.parent_frame()
    time.sleep(1)

    fid = "entryMainFrame"
    frame = _drv.find_element(By.CSS_SELECTOR, f"iframe#{fid}")
    _drv.switch_to.frame(frame)

    save_html(_drv, name=fid, dstring=dstring)


def get_company_info(_drv: webdriver.Ie, wait_time=15) -> Company:
    _wait = WebDriverWait(_drv, wait_time)
    _wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe")))

    fid = "entryTopFrame"
    _wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe#{fid}")))

    tsoup = bs4.BeautifulSoup(_drv.page_source, "html.parser")
    tbody = tsoup.select_one("div.input_table > table > tbody")

    trs = tbody.select("tr")

    _dct = dict()
    for tr in trs:
        ths = tr.select("th")
        ths = list(map(lambda x: x.text.strip(), ths))
        tds = tr.select("td")
        tds = list(map(lambda x: x.text.strip(), tds))
        for k, v in zip(ths, tds):
            k = k.strip()
            v = v.strip()
            _dct[k] = v

    company = Company(
        name=_dct['상호'],
        reg_place=_dct['관할등기소'],
        reg_number=_dct['등기번호'],
        reg_type=_dct['본지점구분'],
        address=_dct['본점 소재지'],
        executives=[]
    )

    _drv.switch_to.parent_frame()

    fid = "entryMainFrame"

    _wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe#{fid}")))

    tbody = _drv.find_element(By.CSS_SELECTOR, "tbody#oTBodyOfficer")
    tsoup = bs4.BeautifulSoup(tbody.get_attribute("innerHTML"), "html.parser")
    trs = tsoup.select("tr")
    for tr in trs:
        tds = tr.select("td")
        tds = list(map(lambda x: x.text.strip(), tds))
        pr = tds[2]
        position, name, *_ = pr.split("/")
        rdate = tds[3]
        reason = tds[4]
        exc = Executive(position=position, name=name, reg_date=rdate, reg_reason=reason)
        company.executives.append(exc)

    a_item_list = _drv.execute_script("return aItemList")
    for item in a_item_list:
        position = item[10]
        name = item[13]
        address = item[16]
        address2 = item[50]
        for e in company.executives:
            if address and position == e.position and name == e.name:
                e.address = f"{address} {address2}"

    _drv.switch_to.parent_frame()
    return company


def find_company(_drv: webdriver.Ie) -> bool:
    targets = _drv.find_elements(By.CSS_SELECTOR, "div.if_list_table.margin5_b > table tbody tr")
    selected = -1
    for n, tr in enumerate(targets[1:]):
        tds = tr.find_elements(By.CSS_SELECTOR, "td")
        info = tds[1].text.strip()
        _type = tds[2].text.strip()
        state = tds[3].text.strip()
        region = tds[4].text.strip()
        if '지점' in _type:
            continue
        if '본점' in _type:
            if '현행등기부' in state and '살아있는' in state:
                selected = n + 1
                print(info, _type, state, region)
    if selected == -1:
        return False
    else:
        targets[selected].click()
        return True


def check_if_browser_is_ready(_drv: webdriver.Ie):
    for i in range(10):
        try:
            print(_drv.title)
            return
        except:
            time.sleep(1)
    else:
        raise Exception


def check_if_alert_exists(_drv: webdriver.Ie, wait_time=1, times=5) -> str:
    _wait = WebDriverWait(_drv, wait_time)
    result = None
    start = time.time()
    for i in range(times):
        for n, handle in enumerate(_drv.window_handles):
            try:
                _drv.switch_to.window(handle)
                _wait.until(EC.alert_is_present())
                alert = _drv.switch_to.alert
                result = alert.text
                alert.accept()
                break
            except NoSuchWindowException:
                time.sleep(1)
            except TimeoutException:
                time.sleep(1)
            finally:
                end = time.time()
    return result


def check_if_window_closed(_drv: webdriver.Ie, handle):
    return not handle in _drv.window_handles


def select_process(drv: webdriver.Ie, start_index, end_index, target_number=None) -> ProcessResult:
    current = start_index
    result = ProcessResult(current=current, target=target_number)
    try:
        _wait = WebDriverWait(drv, 15)

        actions = ActionChains(drv)

        drv.get(f'{BASE_URL}/efrontservlet?cmd=EC2GetBfPayListC&work_cls=E')

        for i in range(10):
            if target_number:
                _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sbtn_bg02_action")))
                target = _wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{target_number}')]")))
                target.click()
            else:
                find_and_click_button_with_text(drv, '신규')
            time.sleep(2)
            if not "/efrontservlet?cmd=EC2GetBfPayListC&work_cls=E" in drv.current_url:
                break
        else:
            raise Exception

        select_type_tage = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select#id_corp_cls")))
        actions.move_to_element(select_type_tage).pause(3)

        find_select_and_click_option(drv, "select#id_corp_cls", '주식회사')
        find_select_and_click_option(drv, "select#id_rgs_type_cd", '변경등기')

        select_type2_tage = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select#id_rgs_type_cd")))
        actions.move_to_element(select_type2_tage).pause(1)

        while 1:
            input_button = _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#corpImg2")))
            actions.move_to_element(input_button).pause(1).perform()

            for i in range(10):
                find_and_click_button(drv, "button#corpImg2")  # 대상법인입력
                select_window(drv, "대상법인검색(등기번호)", exception=False)
                time.sleep(2)
                if "대상법인검색(등기번호)" in drv.title:
                    break
            else:
                raise Exception

            find_select_and_click_option(drv, "select#id_regt_no", '서울중앙지방법원  등기국')

            while 1:
                find_input_and_send_keys(drv, "input#id_dg_no", current)
                find_and_click_button(drv, "button.sbtn_bg02_action")  # 검색버튼

                check = find_company(drv)
                if check:
                    find_and_click_button(drv, "button#btn_select")  # 선택버튼
                    try:
                        WebDriverWait(drv, 5).until(EC.number_of_windows_to_be(3))
                        select_window(drv, "신청사건 계류정보 확인")
                        find_and_click_button_with_text(drv, "확인")
                    except:
                        alert_text = check_if_alert_exists(drv)
                        if alert_text and '해상간주' in alert_text:
                            check_if_alert_exists(drv)
                    WebDriverWait(drv, 15).until(EC.number_of_windows_to_be(1))
                    drv.switch_to.window(drv.window_handles[-1])
                    break
                if current == end_index:
                    break
                current += 1
                result.current = current
                time.sleep(0)

            if current == end_index:
                break

            select_window(drv, "신청서작성현황")

            find_select_and_click_option(drv, "select#id_rgs_rsn_cd", '(대표)이사/감사 등의 임원사항 변경')

            find_input_and_send_keys(drv, "textarea#rgs_rsn", "1")

            isoup = bs4.BeautifulSoup(drv.page_source, "html.parser")
            target_tag = isoup.select_one("input[name='enr_recev_no']")
            target_number = target_tag.attrs['value'] if 'value' in target_tag.attrs and target_tag.attrs[
                'value'] else None
            result.target = target_number

            find_and_click_button(drv, "input#id_chk_form_delete")

            for i in range(10):
                try:
                    find_and_click_button(drv, "button#button_next")
                    try:
                        WebDriverWait(drv, 3).until(EC.number_of_windows_to_be(2))
                        drv.switch_to.window(drv.window_handles[-1])
                        WebDriverWait(drv, 3).until(EC.title_contains("예외사항내역"))
                        find_and_click_button_with_xpath(drv, "//img[@alt='창닫기']/..")
                        WebDriverWait(drv, 3).until(EC.number_of_windows_to_be(1))
                        drv.switch_to.window(drv.window_handles[-1])
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
                find_and_click_button(drv, "button#Entry")
                try:
                    _wait.until(EC.number_of_windows_to_be(2))
                    break
                except:
                    pass

            select_window(drv, "등기할사항")

            company = get_company_info(drv)
            result.companies.append(company)

            current_handle = drv.current_window_handle
            for i in range(10):
                find_and_click_button_with_xpath(drv, "//img[@alt='창닫기']/..")
                time.sleep(2)
                if check_if_window_closed(drv, current_handle):
                    break
            else:
                raise Exception
            select_window(drv, "신청서작성현황")

            if current == end_index:
                break

            for i in range(3):
                find_and_click_button_with_text(drv, '이전')
                try:
                    WebDriverWait(drv, 10).until(EC.url_contains("cmd=EC2GetWriteApplStep1C"))
                    break
                except:
                    pass
            else:
                raise Exception
            current += 1
            result.current = current
    except:
        drv.quit()
    finally:
        return result


def select_doc_with_number(drv: webdriver.Ie, number):
    _wait = WebDriverWait(drv, 15)

    actions = ActionChains(drv)

    drv.get(f'{BASE_URL}/efrontservlet?cmd=EC2GetBfPayListC&work_cls=E')
    _wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sbtn_bg02_action")))

    target = _wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{number}')]")))
    target.click()


def set_protected_mode(enable=True):
    value = 0 if enable else 3
    zones = {
        "a": r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\3",
        "b": r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1",
        "c": r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\2",
        "d": r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\4",
    }

    for zone_name, zone_path in zones.items():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, zone_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "2500", 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)
        except Exception as e:
            pass


def set_intranet_autodetect(enable=True):
    value = 1 if enable else 0

    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "AutoDetect", 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
    except Exception as e:
        pass


def empty_file(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("")


def save_company(cmp: Company, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(cmp.to_string())


def get_last_company(path) -> Company:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = list(filter(lambda x: x, content.split("\n")))
            last = lines[-1].strip()
            result = string_to_company(last)
            return result
    except:
        return None
