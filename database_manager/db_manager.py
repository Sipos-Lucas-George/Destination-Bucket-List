import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


class DB_Manager:
    __database = os.getenv('DATABASE_NAME')
    __admin = os.getenv('DATABASE_ADMIN')
    __user_table = os.getenv('DATABASE_TABLE_LOGIN')
    __favourite_table = os.getenv('DATABASE_TABLE_FAVOURITE')
    __destination_table = os.getenv('DATABASE_TABLE_DESTINATION')

    def signup(self, username, password):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'select * from {self.__user_table} where username=?'
            cur.execute(query, [username])
            if cur.fetchone() is None:
                query = f'insert into {self.__user_table} (username, password) values (?, ?)'
                user_info = (username, password)
                cur.execute(query, user_info)
                query = f'insert into {self.__favourite_table} (user_id, destination_id) values (?, ?)'
                favourite = (cur.lastrowid, -1)
                cur.execute(query, favourite)
                return True
            return False

    def login(self, username):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'select * from {self.__user_table} where username=?'
            cur.execute(query, [username])
            try:
                query_data = cur.fetchone()
                return query_data
            except TypeError:
                return None

    def private_list_add(self, fields):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'insert into {self.__destination_table} ' \
                    f'(user_id, geolocation, title, image, description, start_vacation, end_vacation) ' \
                    f'values (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(query, fields)
            return cur.lastrowid

    def private_list_delete(self, index):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'delete from {self.__destination_table} where id=?'
            cur.execute(query, [index])

    def private_list_update(self, *fields):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'update {self.__destination_table} set geolocation=?, title=?, image=?, description=?, start_vacation=?, end_vacation=? where id=?'
            cur.execute(query, fields)

    def private_list_populate(self, user_id):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'select * from {self.__destination_table} where user_id=?'
            cur.execute(query, [user_id])
            return cur.fetchall()

    def to_private_list_add(self, user_id, destination):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'insert into {self.__destination_table} ' \
                    f'(user_id, geolocation, title, image, description, start_vacation, end_vacation) ' \
                    f'values (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(query, [user_id, destination.geolocation, destination.title, destination.image,
                                destination.description, destination.start_date, destination.end_date])
            return cur.lastrowid

    def public_list_delete(self, user_id):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'update {self.__favourite_table} set destination_id=-1 where user_id=?'
            cur.execute(query, [user_id])

    def public_list_populate(self):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'select destination_id from {self.__favourite_table} where destination_id!=-1'
            cur.execute(query)
            destination_ids = cur.fetchall()
            destination_ids = tuple([item[0] for item in destination_ids])
            if len(destination_ids) != 0:
                cur = connect.cursor()
                if len(destination_ids) == 1:
                    query = f'select * from {self.__destination_table} where id = {destination_ids[0]}'
                else:
                    query = f'select * from {self.__destination_table} where id in {destination_ids}'
                cur.execute(query)
                return cur.fetchall()

    def get_favourite(self, user_id):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'select * from {self.__favourite_table} where user_id=?'
            cur.execute(query, [user_id])
            return cur.fetchone()

    def get_usernames(self, user_ids):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            if len(user_ids) == 1:
                query = f'select id,username from {self.__user_table} where id={user_ids[0]}'
            else:
                query = f'select id,username from {self.__user_table} where id in {user_ids}'
            cur.execute(query)
            return cur.fetchall()
    def set_favourite(self, data):
        with sqlite3.connect(self.__database) as connect:
            cur = connect.cursor()
            query = f'update {self.__favourite_table} set destination_id = ? where user_id=?'
            cur.execute(query, data)
