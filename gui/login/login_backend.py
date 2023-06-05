import os

from PyQt5.QtWidgets import QDialog, QStackedWidget
from gui.login.login import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from gui.list_selector.list_selector_backend import List_Selector
from database_manager.db_manager import DB_Manager
from service.service import Service

from dotenv import load_dotenv

load_dotenv()


class Login_Code(QDialog, Ui_Dialog):
    def __init__(self, stack_widget: QStackedWidget, service: Service, list_selector: List_Selector):
        super(Login_Code, self).__init__()
        self.__stack_widget = stack_widget
        self.setupUi(self)
        self.connect()
        self.__list_selector = list_selector
        self.__service = service
        self.__service.populate_public()
        self.__admin = os.getenv('DATABASE_ADMIN')

    def connect(self):
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button.clicked.connect(self.login_function)
        self.back.clicked.connect(self.go_back)
        self.back.clicked.connect(self.refresh)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.login_function()

    def login_function(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        if len(password) == 0 or len(username) == 0:
            self.warning_label.setText("Input in all necessary fields")
        else:
            query_data = DB_Manager().login(username)
            if query_data is not None and query_data[-1] == password:
                self.create_list_selector(query_data[1] != self.__admin, query_data[0])
            else:
                self.warning_label.setText("Invalid username or password")

    def create_list_selector(self, type_of_user, user_id):
        if user_id != self.__service.user_id:
            self.__list_selector.type_of_user(type_of_user)
            self.__service.clear_repo()
            self.__service.set_user_id(user_id if self.username_line_edit.text() != self.__admin else -1)
        self.refresh()
        self.__stack_widget.setCurrentIndex(3)

    def refresh(self):
        self.username_line_edit.setFocus()
        self.warning_label.setText(None)
        self.username_line_edit.setText(None)
        self.password_line_edit.setText(None)

    def go_back(self):
        self.__stack_widget.setCurrentIndex(0)
