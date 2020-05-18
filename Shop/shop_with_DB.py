import re
from random import randint
from abc import ABC
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from ShopDB import ShopDB, GoodsDB, GoodsInShopDB


shopDB = ShopDB()
goodsDB = GoodsDB()
goods_in_shopDB = GoodsInShopDB()


class StrValue(Exception):
    pass


class NegativeValue(Exception):
    pass


class Address:
    def __init__(self, address):
        lookfor = r"\. ([а-яА-Я]+), ул\. ([а-яА-Я\d-]+), д\. ([\d\/]+)"
        result = re.findall(lookfor, address)
        self.city = result[0][0]
        self.street = result[0][1]
        self.house = result[0][2]

        self.longitude = randint(0, 200)
        self.latitude = randint(0, 200)

    def calculate_distance(self):
        return (self.longitude ** 2 + self.latitude ** 2) ** 0.5

    def __lt__(self, other):
        if isinstance(other, Address):
            return self.calculate_distance() < other.calculate_distance()


class Money:
    def __init__(self):
        self.shop_earnings = defaultdict(int)
        self.total_earnings = 0

    def calculate_earnings(self, shop, goods, amount):
        self.total_earnings += shop.goods_list[goods][0].get_price() * amount
        self.shop_earnings[shop] += shop.goods_list[goods][0].get_price() * amount


class Shop(Address):
    shops = []
    money = Money()

    def __init__(self, address, name):
        super().__init__(address)

        self.address = address

        self.name = name
        self.__class__.shops.append(self)
        self.goods_list = dict()

        ShopDB.insert(self.name, self.address, self.longitude, self.latitude)
        self.shop_id = ShopDB.get_shop_id(self.name)

    def __repr__(self):
        if getattr(self, 'name', None):
            name = self.name
            return f'{name}'

    def add_goods(self, goods, amount):
        if type(amount) == str:
            raise StrValue('Value cannot be a string.')
        if amount < 0:
            raise NegativeValue('Cannot be negative.')
        self.goods_list[goods.name] = [goods, goods.barcode, amount]
        goods_in_shopDB.insert(self.shop_id, goods.goods_id, amount)

        goods.goods_amount += amount

    def find_nearest(self, goods_name):
        other_shops = []
        for shop in self.shops:
            # проверяем наличие товара в магазинах
            if goods_name in shop.goods_list and shop.goods_list[goods_name][2] > 0:
                other_shops.append(shop)
        if other_shops:
            shops_distance = {}
            for shop in other_shops:
                # считаем дистанцию от каждого магазина до нашего
                shops_distance[shop] = [abs(shop.calculate_distance() - self.calculate_distance())]
            min_distance = min(shops_distance.values())  # находим из них минимальную дистанцию до нашего
            closest_shop = [k for k, v in shops_distance.items() if v == min_distance][0]

            return closest_shop
        else:
            return None

    def sale(self, goods_name, amount):
        goods_class = self.goods_list[goods_name][0]  # достаем класс товара для удаление его кол-ва из списка товаров
        amount_in_shop = self.goods_list[goods_name][2]
        if goods_name in self.goods_list and amount <= self.goods_list[goods_name][2]:
            print(f'В магазине {self.goods_list[goods_name][2]} товара')
            self.goods_list[goods_name][2] = self.goods_list[goods_name][2] - amount
            goods_in_shopDB.update(self.shop_id, goods_class.goods_id, self.goods_list[goods_name][2])

            self.__class__.money.calculate_earnings(self, goods_name, amount)
            print(f'Товар {goods_name} в количестве {amount} продан')
            goods_class.goods_amount -= amount
        elif goods_name in self.goods_list and amount > self.goods_list[goods_name][2]:
            print(f'В магазине {self.goods_list[goods_name][2]} ед. {goods_name}')
            self.goods_list[goods_name][2] -= amount_in_shop  # обнуляем кол-во данного товара в магазине
            goods_in_shopDB.update(self.shop_id, goods_class.goods_id, self.goods_list[goods_name][2])
            print('DB updated')
            self.__class__.money.calculate_earnings(self, goods_name, amount_in_shop)
            print(f'Товар {goods_name} в количестве {amount_in_shop} продан')
            closest_shop = self.find_nearest(goods_name)
            if closest_shop:
                closest_address = []
                for shop in self.shops:
                    if str(shop.name) == str(closest_shop):
                        closest_address.append(shop.city)
                        closest_address.append(shop.street)
                        closest_address.append(shop.house)
                print(f"Товара {goods_name} в количестве {amount} нет в данном магазине, "
                      f"ближайший магазин - '{closest_shop}', по адресу г. {closest_address[0]},"
                      f"ул. {closest_address[1]}, д. {closest_address[2]}")
                goods_class.goods_amount -= amount_in_shop
                print(f'Осталось чая всего {goods_class.goods_amount}')
            else:
                goods_class.goods_amount -= amount_in_shop
                print(f'Товара {goods_name} в количестве {amount} нет ни в одном магазине')

    def show_earnings(self):
        if self in self.__class__.money.shop_earnings:
            print(f'Магазин {self} заработал {self.__class__.money.shop_earnings[self]} рублей, '
                  f'всего заработано: {self.__class__.money.total_earnings}')
        else:
            print(f'Магазин "{self}" заработал 0 рублей')

    @staticmethod
    def show_map():
        shops_names = []
        x = []
        y = []
        for shop in __class__.shops:
            x.append(shop.latitude)
            y.append(shop.longitude)
            shops_names.append(shop.name)
        borders = [0, 255]
        rgb = np.random.rand(len(shops_names), 3)  # чтобы разные цвета были
        plt.scatter(x, y, s=60, c=rgb, marker="*")
        plt.scatter(borders, borders, c='white')
        plt.title('Shops map')
        plt.xlabel('latitude')
        plt.ylabel('longitude')

        for i in range(len(shops_names)):
            plt.annotate(f'{shops_names[i].title()}\n({x[i]},{y[i]})', (x[i] - 10, y[i] + 6), fontsize=10)
        plt.show()


class Goods(ABC):
    price = 0
    goods_amount = 0

    def get_price(self):
        return self.price

    def set_price(self, value):
        if type(value) == str:
            raise StrValue('Value cannot be a string.')
        if value < 0:
            raise NegativeValue('Cannot be negative.')
        setattr(self, 'price', value)

    def get_count(self):
        return self.goods_amount

    def __add__(self, value):
        if type(value) == str:
            raise StrValue('Value cannot be a string.')
        if value < 0:
            raise NegativeValue('Cannot be negative.')
        self.goods_amount += value

    def __sub__(self, value):
        self.goods_amount -= value


class Singleton(type(ABC)):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance


class Tea(Goods, metaclass=Singleton):
    __metaclass__ = Singleton

    def __init__(self, name, barcode):
        self.name = name.lower()
        self.barcode = barcode

        goodsDB.insert(self.name, self.barcode)
        self.goods_id = goodsDB.get_goods_id(self.name)

    def __repr__(self):
        return f'{self.__class__.__name__}'


if __name__ == '__main__':
    shop1 = Shop('г. Минск, ул. Гая, д. 54', 'Слоник')
    shop2 = Shop('г. Минск, ул. Молодежная, д. 35', 'Радуга')
    shop3 = Shop('г. Минск, ул. Лесная, д. 2', 'Полянка')
    greenfield = Tea('Greenfield', 115484787)

    shop1.add_goods(greenfield, 55)
    shop2.add_goods(greenfield, 100)
    shop3.add_goods(greenfield, 15)
    greenfield.set_price(27)
    shop1.sale('greenfield', 555)
    print(greenfield.get_count())
    shop2.sale('greenfield', 150)
    print(greenfield.get_count())
    shop3.sale('greenfield', 150)
    shop1.show_earnings()
    shop2.show_earnings()
    shop3.show_earnings()
    Shop.show_map()