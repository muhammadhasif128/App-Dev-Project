class Card:
    count_id = 0
    def __init__(self,firstname,lastname,card_id,date_created,lifespan,expiry_date,email):
        Card.count_id += 1
        self.__name = firstname
        self.__lastname = lastname
        self.__counter = Card.count_id
        self.__card_id = card_id
        self.__date_created = date_created
        self.__lifespan = lifespan
        self.__expiry_date = expiry_date
        self.__email = email
        self.__tokens = 0

    def get_name(self):
        return self.__name

    # Updated
    def set_lastname(self, lname):
        self.__lastname = lname
    def get_lastname(self):
        return self.__lastname

    def get_tokens(self):
        return self.__tokens

    def set_tokens(self,tokens):
        self.__tokens = self.__tokens + tokens

    def bought_tokens(self,costs):
        self.__tokens = self.__tokens - costs
        return self.__tokens

    def get_email(self):
        return self.__email

    def set_email(self,email):
        self.__email = email

    def get_counter(self):
        return self.__counter

    def get_card_id(self):
        return self.__card_id

    def get_date_created(self):
        return self.__date_created

    def get_lifespan(self):
        return self.__lifespan

    def get_expiry_date(self):
        return self.__expiry_date

    def set_name(self,name):
        self.__name = name

    def set_counter(self,counter):
        self.__counter = counter

    def set_card_id(self,card_id):
        self.__name = card_id

    def set_date_created(self,date_created):
        self.__date_created = date_created

    def set_lifespan(self,lifespan):
        self.__lifespan = lifespan

    def set_expiry_date(self,expiry_date):
        self.__expiry_date = expiry_date
