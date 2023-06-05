from exception.exception import *


class Repository:
    def __init__(self):
        self.__data = {}

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data[item]

    def __delitem__(self, key):
        del self.__data[key]

    def __len__(self):
        return len(self.__data)

    def add(self, entity_id, entity):
        if entity_id in self.__data:
            raise Repository_Error("Entity with ID " + str(entity_id) + " already in repository!")
        self.__data[entity_id] = entity

    def delete(self, entity_id):
        if entity_id not in self.__data:
            raise Repository_Error("Entity with ID " + str(entity_id) + " does not exist!")
        del self.__data[entity_id]

    def delete_list_style(self, index):
        if index >= len(self.__data) or index < 0:
            raise Repository_Error("Index not in range of repository length")
        del self.__data[list(self.__data.keys())[index]]

    def update(self, entity_id, new_entity):
        if entity_id not in self.__data:
            raise Repository_Error("Entity with ID " + str(entity_id) + " does not exist!")
        self.__data[entity_id] = new_entity

    def update_list_style(self, index, new_entity):
        if index >= len(self.__data) or index < 0:
            raise Repository_Error("Index not in range of repository length")
        self.__data[list(self.__data.keys())[index]] = new_entity

    def get_keys(self):
        return list(self.__data.keys())

    def get_values(self):
        return list(self.__data.values())

    def get_all(self):
        return self.__data
