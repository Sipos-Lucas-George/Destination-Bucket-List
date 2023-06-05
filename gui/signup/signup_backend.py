from PyQt5.QtWidgets import QDialog, QStackedWidget
from gui.signup.signup import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from database_manager.db_manager import DB_Manager


class Signup_Code(QDialog, Ui_Dialog):
    def __init__(self, stack_widget: QStackedWidget):
        super(Signup_Code, self).__init__()
        self.__stack_widget = stack_widget
        self.setupUi(self)
        self.connect()

    def connect(self):
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_conf_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_button.clicked.connect(self.signup_function)
        self.back.clicked.connect(self.go_back)
        self.back.clicked.connect(self.refresh)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.signup_function()

    def signup_function(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        password_confirm = self.password_conf_line_edit.text()
        if len(password) == 0 or len(username) == 0 or len(password_confirm) == 0:
            self.warning_label.setText("Input in all necessary fields")
        elif password != password_confirm:
            self.warning_label.setText("Passwords do not match")
        elif len(password) < 8 or len(username) < 8:
            self.warning_label.setText("Fields length greater than 8 characters")
        elif not DB_Manager().signup(username, password):
            self.warning_label.setText("Username already exists")
        else:
            self.__stack_widget.setCurrentIndex(2)

    def refresh(self):
        self.username_line_edit.setFocus()
        self.warning_label.setText(None)
        self.username_line_edit.setText(None)
        self.password_line_edit.setText(None)
        self.password_conf_line_edit.setText(None)

    def go_back(self):
        self.__stack_widget.setCurrentIndex(0)
