from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QProgressBar, QPushButton, QSizePolicy,
                               QSpacerItem, QStatusBar, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(703, 354)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(30, 0))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(30, 0))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit_2)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)

        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_3)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lineEdit_4)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBox_2 = QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_3.addWidget(self.checkBox_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.lineEdit_6 = QLineEdit(self.groupBox_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMinimumSize(QSize(10, 0))
        self.lineEdit_6.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_6.setMaxLength(3000)
        self.lineEdit_6.setFrame(True)
        self.lineEdit_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_6)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 0, 3, 1, 1)

        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)

        self.lineEdit_5 = QLineEdit(self.groupBox_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_5, 0, 1, 1, 2)

        self.pushButton_3 = QPushButton(self.groupBox_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 1, 3, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(50, 0))
        self.label_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_6)

        self.lineEdit_7 = QLineEdit(self.groupBox_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setEnabled(False)
        self.lineEdit_7.setAlignment(Qt.AlignCenter)
        self.lineEdit_7.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_7)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(70, 0))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.lineEdit_8 = QLineEdit(self.groupBox_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setEnabled(False)
        self.lineEdit_8.setAlignment(Qt.AlignCenter)
        self.lineEdit_8.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_8)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(50, 0))
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.lineEdit_9 = QLineEdit(self.groupBox_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setEnabled(False)
        self.lineEdit_9.setAlignment(Qt.AlignCenter)
        self.lineEdit_9.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_9)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(50, 0))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_9)

        self.lineEdit_10 = QLineEdit(self.groupBox_3)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setEnabled(True)
        self.lineEdit_10.setFrame(False)
        self.lineEdit_10.setAlignment(Qt.AlignCenter)
        self.lineEdit_10.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.lineEdit_10)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 50))
        self.progressBar.setValue(24)

        self.verticalLayout_3.addWidget(self.progressBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.openFileClicked)
        self.pushButton_2.clicked.connect(MainWindow.startClicked)
        self.pushButton_3.clicked.connect(MainWindow.cancelClicked)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"User Info", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PW", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"hidden", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Parsing Info", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow",
                                                                u"\uc11c\uc6b8\uc911\uc559\uc9c0\ubc29\ubc95\uc6d0 \ub4f1\uae30\uad6d",
                                                                None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"~", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Append File", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Delay", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"State", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Current", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Last Item", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Order", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"State", None))
