import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog
from gui.welcome.welcome_backend import WelcomeCode
from gui.login.login_backend import Login_Code
from gui.signup.signup_backend import Signup_Code
from gui.list_selector.list_selector_backend import List_Selector
from gui.private_list.private_list_backend import Private_List
from gui.public_list.public_list_backend import Public_List
from repository.repository import Repository
from service.service import Service
from PyQt5.QtWidgets import QDesktopWidget


class Center(QDialog):
    def __init__(self):
        super().__init__()

    def center(self):
        qtRectangle = self.frameGeometry()
        qtRectangle.setRight(1600)
        qtRectangle.setBottom(900)
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        return qtRectangle.topLeft()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    repository_private_list = Repository()
    repository_public_list = Repository()
    service = Service(repository_private_list, repository_public_list)
    stack_widget = QStackedWidget()
    ui = WelcomeCode(stack_widget)
    signup = Signup_Code(stack_widget)
    private_list = Private_List(stack_widget, service)
    public_list = Public_List(stack_widget, service)
    selector = List_Selector(stack_widget, service, private_list, public_list)
    login = Login_Code(stack_widget, service, selector)
    stack_widget.setFixedWidth(1600)
    stack_widget.setFixedHeight(900)
    stack_widget.setWindowTitle("Vacation Destination")
    stack_widget.addWidget(ui)
    stack_widget.addWidget(signup)
    stack_widget.addWidget(login)
    stack_widget.addWidget(selector)
    stack_widget.addWidget(private_list)
    stack_widget.addWidget(public_list)
    stack_widget.move(Center().center())
    stack_widget.show()
    sys.exit(app.exec_())
