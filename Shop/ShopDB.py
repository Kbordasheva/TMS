import sqlite3


class ShopDB:
    @staticmethod
    def insert(name, address, longitude, latitude):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''INSERT INTO SHOPS (name, address, longitude, latitude) VALUES (?, ?, ?, ?)''',
                    (name, address, longitude, latitude)
                    )
        connector.commit()
        connector.close()

    @staticmethod
    def get_shop_id(name):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''SELECT shop_id FROM SHOPS WHERE name = ?''', (name,))

        shops_list = []

        rows = cur.fetchall()

        for row in rows:
            shops_list.append(row)

        shop_id = shops_list[-1][0]

        connector.commit()
        connector.close()

        return shop_id


class GoodsDB:
    @staticmethod
    def insert(goods_name, barcode):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''INSERT INTO GOODS (goods_name, barcode) VALUES (?, ?)''',
                    (goods_name, barcode))
        connector.commit()
        connector.close()


    @staticmethod
    def get_goods_id(product):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''SELECT goods_id FROM GOODS WHERE goods_name = ?''', (product,))

        goods_list = []

        rows = cur.fetchall()

        for row in rows:
            goods_list.append(row)

        good_id = goods_list[-1][0]

        connector.commit()
        connector.close()

        return good_id


class GoodsInShopDB:
    @staticmethod
    def insert(shop_id, goods_id, amount):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''INSERT INTO GOODS_IN_SHOP (shop_id, goods_id, amount)  VALUES (?, ?, ?)''',
                    (shop_id, goods_id, amount))
        connector.commit()
        connector.close()

    @staticmethod
    def update(shop_id, goods_id, amount):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''UPDATE GOODS_IN_SHOP SET amount = ? WHERE shop_id = ? AND goods_id = ?''',
                    (amount, shop_id, goods_id))

        connector.commit()
        connector.close()

    @staticmethod
    def show_goods_in_shop(shop_id):
        connector = sqlite3.connect('shops_db.sqlite')
        cur = connector.cursor()

        cur.execute('''SELECT SHOPS.name, GOODS.goods_name, GOODS.barcode, GOODS_IN_SHOP.amount  
        from GOODS_IN_SHOP JOIN SHOPS on SHOPS.shop_id = GOODS_IN_SHOP.shop_id JOIN GOODS on GOODS.goods_id = 
        GOODS_IN_SHOP.goods_id WHERE GOODS_IN_SHOP.shop_id = ?''', (shop_id,))

        rows = cur.fetchall()
        for row in rows:
            print(row)

        connector.commit()
        connector.close()