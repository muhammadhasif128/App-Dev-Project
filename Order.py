class Order:
    count = 0
    def __init__(self, burger, drink, side, costs, name, walletID,address, postcode):
        Order.count += 1
        self.__count = Order.count
        self.__burger = burger
        self.__drink = drink
        self.__side = side
        self.__costs = costs
        self.__name = name
        self.__walletID = walletID
        self.__address = address
        self.__postcode = postcode


    def get_burger(self):
        return self.__burger

    def get_drink(self):
        return self.__drink

    def get_side(self):
        return self.__side

    def get_address(self):
        return self.__address

    def get_costs(self):
        return self.__costs

    def get_wallet(self):
        return self.__walletID

    def get_order_id(self):
        return self.__count
