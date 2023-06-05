from PyQt5.QtWidgets import QDialog, QStackedWidget
from gui.welcome.welcome import Ui_Dialog


class WelcomeCode(QDialog, Ui_Dialog):
    def __init__(self, stack_widget: QStackedWidget):
        super(WelcomeCode, self).__init__()
        self.__stack_widget = stack_widget
        self.setupUi(self)
        self.connect()

    def connect(self):
        self.login_button.clicked.connect(self.go_to_login)
        self.signup_button.clicked.connect(self.go_to_signup)

    def go_to_login(self):
        self.bg_widget.setFocus()
        self.__stack_widget.setCurrentIndex(2)

    def go_to_signup(self):
        self.bg_widget.setFocus()
        self.__stack_widget.setCurrentIndex(1)
