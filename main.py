import re
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QMessageBox, QStyledItemDelegate, QFileDialog, \
    QDateEdit
from PySide6.QtGui import QIcon, QIntValidator, QDoubleValidator

from iros_threads import ProcessThread, SendMessageEvent, FinishEvent, UpdateEvent
from iros_ui import Ui_MainWindow
from iros_variables import *

import iros_functions as rf


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.my_icon = QIcon()
        self.my_icon.addFile(f'{PROJECT_PATH}/source/iros_logo.ico')

        self.setWindowIcon(self.my_icon)

        self.setupUi(self)

        self.lineEdit_3.setValidator(QtGui.QIntValidator(1, 100000000, self))
        self.lineEdit_4.setValidator(QtGui.QIntValidator(1, 100000000, self))
        self.lineEdit_6.setValidator(QtGui.QDoubleValidator(0, 10, 1, self))

        self.set_id("b0000")
        self.set_password("BB1199bb")
        self.set_places()

        self.set_start_idx(1)
        self.set_end_idx("")

        self.set_delay(0)

        self.set_current("없음")
        self.set_last_item("없음")
        self.set_order(0, 0, empty=True)
        self.set_progress(0, 100)

        self.set_state("안녕하세요.")

    def openFileClicked(self, event):
        file_path = self.select_directory()
        if file_path:
            if not os.path.exists(file_path):
                _path = os.path.dirname(file_path)
                _target = os.path.basename(file_path)
                filename = f"{_target}.txt"
                _file_path = f"{_path}/{filename}"
                with open(_file_path, "w", encoding="utf-8") as f:
                    f.write("")
                self.set_start_idx("")
                self.set_directory(_file_path)
            else:
                last_item = rf.get_last_company(file_path)
                if last_item:
                    self.set_place(last_item)
                    self.set_start_idx(int(last_item.reg_number) + 1)

                self.set_directory(file_path)
            self.set_end_idx("")
            self.set_append_file(True)

    def startClicked(self, event):
        print("startClicked!")
        print(self.get_place())

        _id = self.get_id()
        password = self.get_password()
        start = self.get_start_idx()
        end = self.get_end_idx()
        path = self.get_directory()
        place = self.get_place()
        hidden = self.get_check_for_hidden()
        append_option = self.get_check_for_append_file()

        if not path:
            self.show_error_dialog("에러", "파일이 선택되지 않았습니다.\n파일을 선택해주세요.")
            return

        if start > end:
            self.show_error_dialog("에러", "시작 번호가 마지막 번호보다 작아야합니다.")
            return

        self.toggle_buttons()
        self.pthread = ProcessThread(
            _id, password,
            start, end,
            place, path,
            hidden=False,
            append_option=append_option)
        self.pthread.sendMessageSignal.connect(self.event_for_sned_message)
        self.pthread.finishSignal.connect(self.event_for_thread_finish)
        self.pthread.updateSignal.connect(self.event_for_update)

        self.pthread.start()

    def cancelClicked(self, event):
        if self.pthread:
            self.pthread.kill()

    def set_append_file(self, state: bool):
        self.checkBox_2.setChecked(state)

    def set_places(self):
        self.comboBox.clear()
        for place in place_list:
            self.comboBox.addItem(place)

    def set_place(self, company: Company = None, txt=''):
        if company:
            place = company.reg_place
        elif txt:
            place = txt
        else:
            place = ""

        if place:
            place = re.sub(r'\s+', '', place)
            for idx in range(self.comboBox.count()):
                origin_txt = self.comboBox.itemText(idx)
                item_txt = re.sub(r'\s+', '', origin_txt)
                if item_txt == place:
                    self.comboBox.setCurrentText(origin_txt)

    def select_directory(self):
        file_dialog = QFileDialog(self)

        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)  # ExistingFile
        file_dialog.setNameFilter("Text files (*.txt)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            return file_path
        else:
            return None

    def set_directory(self, path):
        self.lineEdit_5.setText(path)

    def get_directory(self):
        return self.lineEdit_5.text()

    def get_place(self):
        return self.comboBox.currentText()

    def get_id(self):
        return self.lineEdit.text()

    def set_id(self, _id):
        self.lineEdit.setText(_id)

    def get_password(self):
        return self.lineEdit_2.text()

    def set_password(self, password):
        self.lineEdit_2.setText(password)

    def get_start_idx(self):
        return int(self.lineEdit_3.text())

    def get_end_idx(self):
        return int(self.lineEdit_4.text())

    def set_start_idx(self, idx):
        self.lineEdit_3.setText(str(idx))

    def set_end_idx(self, idx):
        self.lineEdit_4.setText(str(idx))

    def get_delay(self):
        return self.lineEdit_6.text()

    def set_delay(self, delay):
        self.lineEdit_6.setText(str(delay))

    def set_current(self, current):
        self.lineEdit_7.setText(str(current))

    def set_last_item(self, last):
        self.lineEdit_8.setText(str(last))

    def set_order(self, current, total, empty=False):
        if empty:
            self.lineEdit_9.setText("없음")
        else:
            self.lineEdit_9.setText(f"{current} / {total}")

    def set_progress(self, current, total):
        result = 0
        if total != 0:
            result = int(current / total * 100)
        self.progressBar.setValue(result)

    def get_check_for_hidden(self):
        hidden = self.checkBox.isChecked()
        return hidden

    def get_check_for_append_file(self):
        append_file = self.checkBox_2.isChecked()
        return append_file

    def set_state(self, message):
        self.lineEdit_10.setText(message)

    def toggle_buttons(self):
        buttons = [
            self.lineEdit,
            self.lineEdit_2,
            self.comboBox,
            self.lineEdit_3,
            self.lineEdit_4,
            self.lineEdit_6,
            self.checkBox,
            self.checkBox_2,
            self.pushButton,
            self.pushButton_2,
        ]
        state = buttons[0].isEnabled()
        for btn in buttons:
            btn.setEnabled(not state)

    def event_for_sned_message(self, event: SendMessageEvent):
        self.set_state(event.message)

    def event_for_update(self, event: UpdateEvent):
        if event.success:
            self.set_last_item(event.current)
        self.set_order(event.current, event.total)
        self.set_current(event.number)
        self.set_progress(event.current, event.total)

    def event_for_thread_finish(self, event: FinishEvent):
        wtitle = ""
        state_icon = ""
        text = ""

        state = event.state

        if state == ThreadState.COMPLETE:
            wtitle = "완료"
            state_icon = QMessageBox.Icon.NoIcon
            text = "데이터 수집이 정상적으로 완료되었습니다."
            self.lineEdit_2.setText("")
        elif state == ThreadState.CANCELLED:
            wtitle = "취소"
            state_icon = QMessageBox.Icon.Warning
            text = "사용자의 요청에 의해 수집이 중단되었습니다."
        elif state == ThreadState.ERROR:
            wtitle = "에러"
            state_icon = QMessageBox.Icon.Critical
            text = "데이터 수집하는 도중 에러가 발생하였습니다.\n로그파일과 함께 개발자에 문의바랍니다."
            fe = event.error_message
            dstring = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(LOG_PATH, exist_ok=True)
            file = open(f"{LOG_PATH}/log_{dstring}.txt", "w", encoding="utf-8")
            file.write(fe)
            file.close()

        if wtitle:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(wtitle)
            msgBox.setWindowIcon(self.my_icon)
            msgBox.setIcon(state_icon)
            msgBox.setText(text)
            msgBox.exec()
            self.toggle_buttons()

    def show_error_dialog(self, title, text):
        msgBox = QMessageBox()
        state_icon = QMessageBox.Icon.Critical

        msgBox.setWindowTitle(title)
        msgBox.setWindowIcon(self.my_icon)
        msgBox.setIcon(state_icon)
        msgBox.setText(text)
        msgBox.exec()


app = QApplication()
window = MainWindow()
window.setWindowTitle(PROGRAM_TITLE)
window.show()
app.exec()
