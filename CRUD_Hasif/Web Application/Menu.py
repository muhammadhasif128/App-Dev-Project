class Food:
    count = 0
    def __init__(self,type,  name, price, image):
        self.__type = type
        self.__name = name
        self.__price = price
        self.__image = image
        Food.count +=1
        self.__food_id = Food.count

    def set_name(self,name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price

    def set_image(self,image):
        self.__image = image

    def get_image(self):
        return self.__image

    def get_food_id(self):
        return self.__food_id

    def set_food_type(self,type):
        self.__type = type

    def get_food_type(self):
        return self.__type