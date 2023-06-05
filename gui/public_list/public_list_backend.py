import io
import requests
import validators

from PIL import Image

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from gui.public_list.public_list import Ui_Dialog
from service.service import Service


class Public_List(QDialog, Ui_Dialog):
    def __init__(self, stack_widget: QStackedWidget, service: Service):
        super(Public_List, self).__init__()
        self.__stack_widget = stack_widget
        self.__service = service
        self.setupUi(self)
        self.connect()

    def connect(self):
        self.delete_button.clicked.connect(self.focus)
        self.delete_button.clicked.connect(self.delete_destination)
        self.add_button.clicked.connect(self.focus)
        self.add_button.clicked.connect(self.add_destination)
        self.public_list_view.itemClicked.connect(self.set_everything)
        self.back.clicked.connect(self.focus)
        self.back.clicked.connect(self.go_back)

    def populate_view(self):
        self.public_list_view.clear()
        if len(self.__service.get_values_public()) == 0:
            return
        if self.__service.user_id == -1:
            usernames = self.__service.get_usernames()
            for key, value in self.__service.get_all_public().items():
                self.public_list_view.addItem(usernames[key] + ' -> ' + value.to_string())
        else:
            for key, value in self.__service.get_all_public().items():
                if key == self.__service.user_id:
                    self.public_list_view.addItem("📌  " + value.to_string())
                else:
                    self.public_list_view.addItem(value.to_string())

    def delete_destination(self):
        index = self.public_list_view.currentRow()
        if index < 0:
            return
        self.__service.delete_list_style_public(index)
        self.populate_view()

    def add_destination(self):
        index = self.public_list_view.currentRow()
        if self.__service.get_keys_public()[index] != self.__service.user_id:
            self.__service.add_to_private(self.__service.user_id, self.__service.get_values_public()[index])

    def clear_everything(self):
        self.public_list_view.setCurrentRow(-1)

    def set_everything(self):
        index = self.public_list_view.currentRow()
        if index != -1:
            item = self.__service.get_values_public()[index]
            self.set_image(item.image)

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
        self.set_image('')
        self.__stack_widget.setCurrentIndex(3)

    @staticmethod
    def url_is_image(response: requests):
        if 'content-type' not in response.headers:
            return False
        content_type = response.headers['content-type']
        if content_type.startswith('image/'):
            return True
        return False
