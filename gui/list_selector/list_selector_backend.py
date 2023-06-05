from PyQt5.QtWidgets import QDialog, QStackedWidget
from gui.list_selector.list_selector import Ui_Dialog
from gui.private_list.private_list_backend import Private_List
from gui.public_list.public_list_backend import Public_List
from service.service import Service


class List_Selector(QDialog, Ui_Dialog):
    def __init__(self, stack_widget: QStackedWidget, service: Service, private_list: Private_List, public_list: Public_List):
        super(List_Selector, self).__init__()
        self.__stack_widget = stack_widget
        self.__service = service
        self.__private_list = private_list
        self.__public_list = public_list
        self.setupUi(self)
        self.connect()

    def type_of_user(self, user):
        self.private_list_button.setVisible(user)
        self.__public_list.add_button.setVisible(user)
        self.__public_list.delete_button.setVisible(not user)
        self.focus()

    def connect(self):
        self.private_list_button.clicked.connect(self.focus)
        self.private_list_button.clicked.connect(self.private_list_function)
        self.public_list_button.clicked.connect(self.focus)
        self.public_list_button.clicked.connect(self.public_list_function)
        self.back.clicked.connect(self.focus)
        self.back.clicked.connect(self.go_back)

    def public_list_function(self):
        self.focus()
        self.__public_list.populate_view()
        self.__stack_widget.setCurrentIndex(5)
        self.focus()

    def private_list_function(self):
        self.focus()
        self.__private_list.populate_view()
        self.__stack_widget.setCurrentIndex(4)
        self.focus()

    def focus(self):
        self.bg_widget.setFocus()

    def go_back(self):
        self.__stack_widget.setCurrentIndex(2)
