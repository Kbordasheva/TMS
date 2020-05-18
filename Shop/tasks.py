# 1. Необходимо написать программу которая будет отслеживать товар в магазинах.
# 
# 1.1 Адрес
# Для начала нужно создать класс Address. Как входные параметры нужно передать
# строку вида "г. Город, ул. Улица №дома". Необходимо распарсить данную строку
# и достать атрибуты: город, улица, №дома и установить их как атрибуты объекта.
# Установить случайные атрибуты долгота и ширина для каждого экземпляра.
# Добавить возможность сравнивать адреса по долготе и ширине.

# 1.2 Магазин
# Создать класс Shop с предком Address. Каждый новый магазин должен
# записываться в атрибут класса Shop.shops.

# 1.3 Товары
# Создать абстрактный класс Goods. У данного класса должно быть 3 метода:
#   - get_price - вернуть цену товара
#   - set_price - установить цену товара
#   - get_count - вернуть количество товара
# Изначально у товара цена и количество равны 0 (изначальная цена - атрибут
# класса). Переопределите сложение и вычитание для класса Goods для изменения
# количества товара.

# 1.4 Товары разного типа
# Наследуйтесь от Goods и создайте конкретный товар, например чай. Установите
# цену. Каждый товар должен иметь наименование и штрих код.
#
# 1.5 Товары в магазине
# Реализовать добавление товара в магазин. Метод должен принимать товар и его
# количество, которое будет хранится в данном магазине (кол-во товара не может
# быть меньше, чем кол-во товара в магазине).

# 1.6 Продажа
# Реализовать метод sale для класса Shop. Метод должен принимать наименование
# товара и его количество. По наименованию ищется экземпляр товара в магазине.
# Если такой товар существует в магазине, то вычитается запрашиваемое
# количество как в магазине так и в целом для товара. Если запрашиваемое кол-во
#  больше имеющегося, то вычитается всё, что есть. Если в магазине нет такого
# товара, то необходимо вывести адрес ближайшего магазина с таким товаром.
# Если товара нигде нет, то сообщить об этом.

# 1.7 Заработанные деньги
# Ведите подсчёт заработанных денег для каждого магазина и для всех в целом
# используя атрибуты класса и экземпляра money.

# 2.
# 2.1 Расположение магазинов
# Реализовать метод класса для Shops (предудыщий урок), который будет выводить
# расположение всех магазинов на графике (используйте matplotlib).

# 2.2 Запрет неверных значений
# Реализуйте товары из задания для прошлого урока так, чтобы нельзя было
# устанавливать неверное значение для атрибутов цена и количество. Т. е.
# запретить такую возможность tea.price = 'Цена как строка'

# 3. Товары в магазинах

# 3.1 Создать необходимые таблицы.
# Создать 3 таблицы: Shops (id, имя, адрес, долгота, широта),
# Goods (id, имя, штрих код), GoodsInShop (id магазина, id товара, количество).
# Используйте PRIMARY и FOREIGN KEYS для создания таблиц.

# 3.2 Создайте python классы ShopDB, GoodsBD, GoodsInShopDB. Каждый класс должен
# уметь сохранять необходимые данные в соответствующие таблицы. Экземпляр
# класса GoodsInShopDB должен уметь выводить наименование товара, штрих код,
# наименование магазина и количество товара в конкретном магазине (реализовать
# метод).

# 3.3 Совместить с существующим.
# Сохраняйте все изменения для классов Shop и Good из Lesson 10 в БД с помощью
# ShopDB, GoodsBD, GoodsInShopDB (когда создаётся новый экземпляр, запись
# должна записаться в БД; когда товар продан, изменения должны появится в
# БД и т.д.)


