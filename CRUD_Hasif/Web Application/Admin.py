import User


class Admin(User.User):
    count_id = 0

    def __init__(self, first_name, last_name, today_date, age, phone_no, gender, email_address, postal_code, account_status):
        super().__init__(first_name, last_name, today_date, age, phone_no, gender, email_address, postal_code, account_status)
        Admin.count_id += 1
        self.__user_id = Admin.count_id
