from repository.repository import Repository
from model.destination import Destination
from database_manager.db_manager import DB_Manager


class Service:
    def __init__(self, repository_private_list: Repository, repository_public_list: Repository):
        self.__private_list_repo = repository_private_list
        self.__public_list_repo = repository_public_list
        self.__user_id = 0
        self.__favourite = 0

    def __getitem__(self, item):
        return self.__private_list_repo[item]

    def __setitem__(self, key, value):
        self.__private_list_repo[key] = value

    def add(self, *fields):
        id_db = DB_Manager().private_list_add(fields)
        self.__private_list_repo.add(id_db, Destination(*fields[1:]))

    def add_to_private(self, user_id, destination: Destination):
        id_db = DB_Manager().to_private_list_add(user_id, destination)
        self.__private_list_repo.add(id_db, destination)

    def delete(self, entity_id):
        self.__private_list_repo.delete(entity_id)

    def delete_list_style(self, index):
        DB_Manager().private_list_delete(self.get_keys()[index])
        self.__private_list_repo.delete_list_style(index)

    def delete_list_style_public(self, index):
        DB_Manager().public_list_delete(self.get_keys_public()[index])
        self.__public_list_repo.delete_list_style(index)

    def update_list_style(self, index, *fields):
        DB_Manager().private_list_update(*fields, self.get_keys()[index])
        self.__private_list_repo.update_list_style(index, Destination(*fields))

    @property
    def user_id(self):
        return self.__user_id

    @property
    def favourite(self):
        return self.__favourite

    @favourite.setter
    def favourite(self, value):
        DB_Manager().set_favourite([value, self.__user_id])
        if self.__favourite != -1:
            self.__public_list_repo.update(self.__user_id, self.__private_list_repo[value])
        else:
            self.__public_list_repo.add(self.__user_id, self.__private_list_repo[value])
        self.__favourite = value

    def set_user_id(self, user_id):
        self.__user_id = user_id
        self.populate()
        self.get_favourite()

    def populate(self):
        fetch_data = DB_Manager().private_list_populate(self.__user_id)
        if fetch_data is None:
            return
        for data in fetch_data:
            self.__private_list_repo.add(data[0], Destination(*data[2:]))

    def populate_public(self):
        fetch_data = DB_Manager().public_list_populate()
        if fetch_data is None:
            return
        for data in fetch_data:
            self.__public_list_repo.add(data[1], Destination(*data[2:]))

    def get_favourite(self):
        fetch_data = DB_Manager().get_favourite(self.__user_id)
        if fetch_data is not None:
            self.__favourite = fetch_data[1]

    def get_usernames(self):
        fetch_data = DB_Manager().get_usernames(tuple(self.get_keys_public()))
        return {data[0]: data[1] for data in fetch_data}

    def clear_repo(self):
        self.__private_list_repo = Repository()

    def get_keys(self):
        return self.__private_list_repo.get_keys()

    def get_values(self):
        return self.__private_list_repo.get_values()

    def get_all(self):
        return self.__private_list_repo.get_all()

    def get_keys_public(self):
        return self.__public_list_repo.get_keys()

    def get_values_public(self):
        return self.__public_list_repo.get_values()

    def get_all_public(self):
        return self.__public_list_repo.get_all()
