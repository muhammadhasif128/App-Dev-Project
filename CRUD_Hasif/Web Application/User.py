class User:
    count_id = 0

    def __init__(self, first_name, last_name, today_date, age, phone_no, gender, email_address, postal_code, account_status):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__today_date = today_date
        self.__age = age
        self.__phone_no = phone_no
        self.__gender = gender
        self.__email_address = email_address
        self.__postal_code = postal_code
        self.__account_status = account_status

    # get

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_today_date(self):
        return self.__today_date

    def get_age(self):
        return self.__age

    def get_phone_no(self):
        return self.__phone_no

    def get_gender(self):
        return self.__gender

    def get_email_address(self):
        return self.__email_address

    def get_postal_code(self):
        return self.__postal_code

    def get_account_status(self):
        return self.__account_status

    # set

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_today_date(self, today_date):
        self.__today_date = today_date

    def set_age(self, age):
        self.__age = age

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_gender(self, gender):
        self.__gender = gender

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_account_status(self, account_status):
        self.__account_status = account_status


