# Just a draft on what classes we could use
import hashlib


class Staff:
    pass


class Developer(Staff):
    pass


class Support(Staff):
    pass


class User:
    user_id = 0
    def __init__(self, username, email):
        self.__username = username
        self.__email = email
        self.__password = None
        User.user_id += 1

    def set_password(self, password):
        if isalnum(password):
            self.__password = hashlib.sha256(password.encode())
        #password hash, password.hexdigest





class Rewards(User):
    pass
