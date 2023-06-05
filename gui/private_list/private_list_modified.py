from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from gui.private_list.private_list import Ui_Dialog


class Private_List_Modified(Ui_Dialog):
    def __init__(self):
        super().__init__()

    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        layout1 = QtWidgets.QVBoxLayout()
        self.start_date_picker.setLayout(layout1)
        self.start_today_button = QtWidgets.QPushButton('&Today')
        self.start_today_button.setStyleSheet("""background-color: rgb(255, 255, 255);
border-width: 1px;
border-style: solid;
border-radius: 10px;
font-size: 20px;""")
        self.start_date_picker.calendarWidget().layout().addWidget(self.start_today_button)
        self.start_date_picker.calendarWidget().setSelectedDate(QDate().currentDate())
        self.start_date_picker.setMinimumDate(QDate().currentDate())
        layout2 = QtWidgets.QVBoxLayout()
        self.end_date_picker.setLayout(layout2)
        self.end_today_button = QtWidgets.QPushButton('&Today')
        self.end_today_button.setStyleSheet("""background-color: rgb(255, 255, 255);
border-width: 1px;
border-style: solid;
border-radius: 10px;
font-size: 20px;""")
        self.end_date_picker.calendarWidget().layout().addWidget(self.end_today_button)
        self.end_date_picker.calendarWidget().setSelectedDate(QDate().currentDate())
        self.end_date_picker.setMinimumDate(QDate().currentDate())
