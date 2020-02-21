PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS recipies;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS cookies;

PRAGMA foreign_keys=ON;

CREATE TABLE cookies (
  name  TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY
);

CREATE TABLE customers (
  name VARCHAR(99) PRIMARY KEY,
  address VARCHAR(99) NOT NULL
);

CREATE TABLE ingredients (
  name TEXT PRIMARY KEY,
  quantity INTEGER NOT NULL
  inSock Boolean DEFAULT 0, -- Behövs detta?
  unit VARCHAR(99) NOT NULL,
);

CREATE TABLE recipies (
  quantity INTEGER NOT NULL,
  ingredient_name TEXT,
  cookie_name TEXT,
  FOREIGN KEY (ingredient_name) REFERENCES ingredients(name),
  FOREIGN KEY (cookie_name) REFERENCES cookies(name)
);

CREATE TABLE pallets (
  reference TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  productionDate DATE DEFAULT CURRENT_DATE,
  blocked BOOLEAN DEFAULT 0,
  order_reference TEXT,
  FOREIGN KEY (order_reference) REFERENCES orders(reference)
);

CREATE TABLE palletContents (
  pallet_reference TEXT NOT NULL,
  cookie_name TEXT NOT NULL,
  FOREIGN KEY (pallet_reference) REFERENCES pallets(reference)
  FOREIGN KEY (cookie_name) REFERENCES cookies(name)
);

CREATE TABLE orders (
  reference TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  customer_name TEXT NOT NULL,
  FOREIGN KEY (customer_name) REFERENCES customers(name)
);

