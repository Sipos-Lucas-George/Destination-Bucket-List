import io
import requests
import validators

from PIL import Image
from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import *
from gui.private_list.private_list_modified import Private_List_Modified
from service.service import Service
from model.destination import Destination


class Private_List(QDialog, Private_List_Modified):
    def __init__(self, stack_widget: QStackedWidget, service: Service):
        super(Private_List, self).__init__()
        self.__stack_widget = stack_widget
        self.__service = service
        self.setupUi(self)
        self.connect()

    def connect(self):
        self.make_favourite_button.clicked.connect(self.focus)
        self.make_favourite_button.clicked.connect(self.set_favourite_destination)
        self.delete_button.clicked.connect(self.focus)
        self.delete_button.clicked.connect(self.delete_destination)
        self.add_button.clicked.connect(self.focus)
        self.add_button.clicked.connect(self.add_destination)
        self.update_button.clicked.connect(self.focus)
        self.update_button.clicked.connect(self.update_destination)
        self.geolocation_line_edit.textChanged.connect(self.verify_geolocation)
        self.title_line_edit.textChanged.connect(self.verify_title)
        self.image_line_edit.textChanged.connect(self.verify_url_image)
        self.image_line_edit.editingFinished.connect(self.verify_image_response)
        self.image_line_edit.editingFinished.connect(self.refresh_image)
        self.description_line_edit.textChanged.connect(self.verify_description)
        self.start_date_picker.dateChanged.connect(self.set_minimum_end_date)
        self.clear_selection_button.clicked.connect(self.focus)
        self.clear_selection_button.clicked.connect(self.clear_everything)
        self.clear_fields_button.clicked.connect(self.focus)
        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.private_list_view.itemClicked.connect(self.set_everything)
        self.back.clicked.connect(self.focus)
        self.back.clicked.connect(self.go_back)
        self.start_today_button.clicked.connect(self.focus)
        self.start_today_button.clicked.connect(self.set_start_today)
        self.end_today_button.clicked.connect(self.focus)
        self.end_today_button.clicked.connect(self.set_end_today)

    def populate_view(self):
        self.private_list_view.clear()
        index = 0
        for key, value in self.__service.get_all().items():
            if key == self.__service.favourite:
                self.private_list_view.addItem("📌  " + value.to_string())
            else:
                self.private_list_view.addItem(value.to_string())
            index += 1

    def set_favourite_destination(self):
        index = self.private_list_view.currentRow()
        if index >= 0:
            self.__service.favourite = self.__service.get_keys()[index]
            self.populate_view()

    def delete_destination(self):
        index = self.private_list_view.currentRow()
        if index < 0:
            return
        if self.__service.favourite == self.__service.get_keys()[index]:
            self.__service.favourite = -1
        self.__service.delete_list_style(index)
        self.populate_view()

    def add_destination(self):
        if not self.verify_inputs():
            return
        self.__service.add(self.__service.user_id, self.geolocation_line_edit.text(), self.title_line_edit.text(),
                           self.image_line_edit.text(), self.description_line_edit.text(),
                           self.start_date_picker.text(), self.end_date_picker.text())
        self.populate_view()

    def update_destination(self):
        index = self.private_list_view.currentRow()
        if index < 0:
            return
        if not self.verify_inputs():
            return
        self.__service.update_list_style(index, self.geolocation_line_edit.text(), self.title_line_edit.text(),
                                         self.image_line_edit.text(), self.description_line_edit.text(),
                                         self.start_date_picker.text(), self.end_date_picker.text())
        self.populate_view()

    def verify_geolocation(self):
        item_text = self.geolocation_line_edit.text()
        self.change_color_text(self.geolocation_line_edit, len(item_text) < 4)

    def verify_title(self):
        item_text = self.title_line_edit.text()
        self.change_color_text(self.title_line_edit, len(item_text) < 4)

    def verify_url_image(self):
        item = self.image_line_edit.text()
        if not validators.url(item):
            self.change_color_text(self.image_line_edit, True)
            return
        self.change_color_text(self.image_line_edit, False)

    def verify_image_response(self):
        item = self.image_line_edit.text()
        if not validators.url(item):
            self.change_color_text(self.image_line_edit, True)
            return
        response = requests.get(item)
        if not self.url_is_image(response):
            self.change_color_text(self.image_line_edit, True)
            return
        image_data = response.content
        if image_data is None:
            self.change_color_text(self.image_line_edit, True)
            return
        self.change_color_text(self.image_line_edit, False)

    def verify_description(self):
        item_text = self.description_line_edit.text()
        self.change_color_text(self.description_line_edit, len(item_text) < 4)

    def set_minimum_end_date(self):
        self.end_date_picker.setMinimumDate(self.start_date_picker.date())

    def clear_everything(self):
        self.private_list_view.setCurrentRow(-1)

    def set_everything(self):
        index = self.private_list_view.currentRow()
        if index != -1:
            item = self.__service.get_values()[index]
            self.set_fields(item)
            self.set_image(item.image)
        else:
            self.clear_fields()

    def set_fields(self, item: Destination):
        self.geolocation_line_edit.setText(item.geolocation)
        self.title_line_edit.setText(item.title)
        self.image_line_edit.setText(item.image)
        self.description_line_edit.setText(item.description)
        self.start_date_picker.setDate(datetime.strptime(item.start_date, '%d/%m/%Y').date())
        self.end_date_picker.setDate(datetime.strptime(item.end_date, '%d/%m/%Y').date())

    def clear_fields(self):
        self.geolocation_line_edit.clear()
        self.title_line_edit.clear()
        self.image_line_edit.clear()
        self.description_line_edit.clear()
        self.set_start_today()
        self.set_end_today()
        self.set_image('')

    def refresh_image(self):
        self.set_image(self.image_line_edit.text())

    def set_image(self, url):
        self.show_image.setPixmap(QPixmap())
        if not validators.url(url):
            return
        response = requests.get(url)
        if not self.url_is_image(response):
            return
        image_data = response.content
        if image_data is None:
            return
        image_data = io.BytesIO(image_data)
        image_data.seek(0)
        with Image.open(image_data) as img:
            img_without_icc = Image.new("RGB", img.size, (255, 255, 255))
            img_without_icc.paste(img, mask=img.convert("RGBA").split()[-1])
        image = QImage(img_without_icc.tobytes(), img_without_icc.size[0], img_without_icc.size[1],
                       QImage.Format_RGB888)
        if image.isNull():
            return
        self.show_image.setPixmap(QPixmap(image))
        if image.size().width() > 640 or image.size().height() > 480:
            self.show_image.setScaledContents(True)
        else:
            self.show_image.setScaledContents(False)

    def focus(self):
        self.bg_widget.setFocus()

    def go_back(self):
        self.__stack_widget.setCurrentIndex(3)

    def set_start_today(self):
        self.start_date_picker.calendarWidget().setSelectedDate(QDate().currentDate())

    def set_end_today(self):
        self.end_date_picker.calendarWidget().setSelectedDate(QDate().currentDate())

    def verify_inputs(self):
        if self.geolocation_line_edit.palette().color(QPalette.Text) != QColor("black") \
                or self.title_line_edit.palette().color(QPalette.Text) != QColor("black") \
                or self.image_line_edit.palette().color(QPalette.Text) != QColor("black") \
                or self.description_line_edit.palette().color(QPalette.Text) != QColor("black"):
            return False
        return True

    @staticmethod
    def url_is_image(response: requests):
        if 'content-type' not in response.headers:
            return False
        content_type = response.headers['content-type']
        if content_type.startswith('image/'):
            return True
        return False

    @staticmethod
    def change_color_text(item: QLineEdit, value: bool):
        if value:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor("red"))
            item.setPalette(palette)
        else:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor("black"))
            item.setPalette(palette)
