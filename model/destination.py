class Destination:
    def __init__(self, geolocation: str, title: str, image: str, description: str, start_date: str, end_date: str):
        self.__geolocation = geolocation
        self.__title = title
        self.__image = image
        self.__description = description
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def geolocation(self):
        return self.__geolocation

    @geolocation.setter
    def geolocation(self, value):
        self.__geolocation = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    def to_string(self):
        return f'({self.__start_date} -> {self.__end_date})   ' \
               f'{self.__geolocation} - {self.__title} - {self.__description}'

    def __str__(self):
        return f'{self.__geolocation},{self.__title},{self.__description},{self.__start_date},{self.__end_date}'
