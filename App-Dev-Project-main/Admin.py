import User


class Admin(User.User):
    count_id = 0

    def __init__(self, first_name, last_name, today_date, age, phone_no, gender, email_address):
        super().__init__(first_name, last_name, today_date, age, phone_no, gender, email_address, postal_code=None, account_status='Staff')
        Admin.count_id += 1
        self.__staff_id = Admin.count_id

    def get_staff_id(self):
        return self.__staff_id
