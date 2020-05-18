CREATE TABLE IF NOT EXISTS SHOPS (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32),
    address VARCHAR(40),
    longitude INTEGER,
    latitude INTEGER
);

INSERT INTO SHOPS (name, address, longitude, latitude) VALUES (
'Вяселка', 'г. Минск, ул. Гая, д. 5', '545', '451'
                                                              );

INSERT INTO SHOPS (name, address, longitude, latitude) VALUES
('Чайкофф', 'г. Свислочь, ул. Молодежная, д. 26', 214, 231),
('Куку', 'г. Витебск, ул. Сосновая, д. 56', 100, 234);

SELECT * FROM SHOPS;

CREATE TABLE GOODS (
    goods_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goods_name VARCHAR(20),
    barcode INTEGER
);

CREATE TABLE GOODS_IN_SHOP (
    shop_id INTEGER,
    goods_id INTEGER,
    amount INTEGER,
    FOREIGN KEY (shop_id) REFERENCES SHOPS (shop_id),
    FOREIGN KEY (goods_id) REFERENCES GOODS (goods_id)
);

INSERT INTO GOODS (goods_name, barcode) VALUES
('Greenfield', 23255454),
('Neskafe', 54454748),
('Lavazza', 5458745478),
('Tess', 15477454);

SELECT * FROM GOODS;

INSERT INTO GOODS_IN_SHOP (shop_id, goods_id, amount)  VALUES
(1, 1, 20),
(2, 2, 25),
(3, 2, 21),
(2, 4, 20),
(1, 4, 32),
(2, 1, 10);

SELECT * FROM GOODS_IN_SHOP;

SELECT shop_id FROM SHOPS WHERE name = 'Радуга'

DELETE from SHOPS WHERE shop_id>7

UPDATE GOODS_IN_SHOP SET amount = 7 WHERE shop_id = 1 AND goods_id = 2
