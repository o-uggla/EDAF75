import sqlite3

class Database(object):
  def __init__(self, path: str):
    self.conn = sqlite3.connect(path, check_same_thread=False)
    self.c = self.conn.cursor()
    self.c.execute("PRAGMA foreign_keys = ON")

  def get_customers(self):
    keys = ['name', 'address']
    data = self.c.execute("SELECT name, address FROM customers").fetchall()
    res = self.prettierJsonList(keys, data)
    return res

  def get_ingredients(self):
    keys = ['name', 'quantity', 'unit']
    data = self.c.execute("SELECT name, quantity, unit FROM ingredients").fetchall()
    res = self.prettierJsonList(keys, data)
    return res

  def get_cookies(self):
    keys = ['name']
    data = self.c.execute("SELECT name FROM cookies").fetchall()
    res = self.prettierJsonList(keys, data)
    return res

  def get_recipies(self):
    keys = ['cookie', 'ingredient', 'quantity', 'unit']
    data = self.c.execute("""
      SELECT cookie_name, ingredient_name, recipies.quantity, unit
      FROM recipies
      LEFT JOIN ingredients
      ON recipies.ingredient_name = ingredients.name
      ORDER BY cookie_name, ingredient_name ASC
      """).fetchall()
    res = self.prettierJsonList(keys, data)
    return res

  def get_pallets(self):
    keys = ['id', 'cookie', 'productionDate', 'customer', 'blocked']
    data = self.c.execute("""
      SELECT pallets.reference, palletContent.cookie_name, productionDate, customer_name, blocked
      FROM pallets
      LEFT JOIN orders
      ON pallets.order_reference = orders.reference
      LEFT JOIN palletContents
      ON pallets.reference = palletContents.pallet_reference
      ORDER BY pallets.productionDate, palletContent.cookie_name DESC
      """).fetchall()
    res = self.prettierJsonList(keys, data)
    return res
  
  def reset(self):
    cookies = [
      ('Nut ring'),
      ('Nut cookie'),
      ('Amneris'),
      ('Tango'),
      ('Almond delight'),
      ('Berliner')]

    customers = [
        ('Finkakor AB', 'Helsingborg'),
        ('Småbröd AB', 'Malmö'),
        ('Kaffebröd AB', 'Landskrona'),
        ('Bjudkakor AB', 'Ystad'),
        ('Kalaskakor AB', 'Trelleborg'),
        ('Partykakor AB', 'Kristianstad'),
        ('Gästkakor AB', 'Hässleholm'),
        ('Skånekakor AB', 'Perstorp')]

    
    ingredients = [
      ('Flour', '100 000', 'g'),
      ('Butter', '100 000', 'g'),
      ('Icing sugar', '100 000', 'g'),
      ('Roasted, chopped nuts', '100 000', 'g'),
      ('Fine-ground nuts', '100 000', 'g'),
      ('Ground, roasted nuts', '100 000', 'g'),
      ('Bread crumbs', '100 000', 'g'),
      ('Sugar', '100 000', 'g'),
      ('Egg whites', '100 000', 'ml'),
      ('Chocolate', '100 000', 'g'),
      ('Marzipan', '100 000', 'g'),
      ('Eggs', '100 000', 'g'),
      ('Potato starch', '100 000', 'g'),
      ('Wheat flour', '100 000', 'g'),
      ('Sodium bicarbonate', '100 000', 'g'),
      ('Vanilla', '100 000', 'g'),
      ('Chopped almonds', '100 000', 'g'),
      ('Cinnamon', '100 000', 'g'),
      ('Vanilla sugar', '100 000', 'g')]

    recipies =[
      ('Nut ring', 'Flour', '450'),
      ('Nut ring', 'Butter', '450'),
      ('Nut ring', 'Icin sugar', '190'),
      ('Nut ring', 'Roasted, chopped nuts', '225'),
      ('Nut cookie', 'Fine-ground nuts', '750'),
      ('Nut cookie', 'Ground roasted nuts', '625'),
      ('Nut cookie', 'Bread crumbs', '125'),
      ('Nut cookie', 'Sugar', '375'),
      ('Nut cookie', 'Egg whites', '350'),
      ('Nut cookie', 'Chocolate', '50'),
      ('Amneris', 'Marzipan', '750'),
      ('Amneris', 'Butter', '250'),
      ('Amneris', 'Eggs', '250'),
      ('Amneris, Potato starch', '25'),
      ('Amneris, Wheat flour', '25'),
      ('Tango', 'Butter', '200'),
      ('Tango', 'Sugar', '250'),
      ('Tango', 'Flour', '300'),
      ('Tango', 'Sodium bicarbonate', '4'),
      ('Tango', 'Vanilla', '2'),
      ('Almond delight', 'Butter', '400'),
      ('Almond delight', 'Sugar', '270'),
      ('Almond delight', 'Chopped almonds', '279'),
      ('Almond delight', 'Flour', '400'),
      ('Almond delight', 'Cinnamon', '10'),
      ('Berliner', 'Flour', '350'),
      ('Berliner', 'Butter', '250'),
      ('Berliner', 'Icing sugar', '100'),
      ('Berliner', 'Eggs', '50'),
      ('Berliner', 'Vanilla sugar', '5'),
      ('Berliner', 'Chocolate', '50')
    ]

    self.c.execute("DELETE FROM pallets")
    self.c.execute("DELETE FROM recipies")
    self.c.execute("DELETE FROM ingredients")
    self.c.execute("DELETE FROM customers")
    self.c.execute("DELETE FROM cookies")

    self.c.executemany("INSERT INTO cookies(name) values (?)", cookies)
    self.c.executemany("INSERT INTO customers(name, address) values (?,?)", customers)
    self.c.executemany("INSERT INTO ingredients(name, quantity, unit) values (?,?,?)", ingredients)
    self.c.executemany("INSERT INTO recipies(cookie_name, ingredient_name, quantity) values (?,?,?)", recipies)
    
    self.conn.commit()
  def prettierJsonList(self, key, data):
    return [dict(zip(key, d))for d in data]
