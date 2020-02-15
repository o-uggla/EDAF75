-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;

CREATE TABLE users (
  user_id VARCHAR(99) NOT NULL UNIQUE PRIMARY KEY,
  name VARCHAR(99),
  password INTEGER NOT NULL
);

CREATE TABLE movies (
  title VARCHAR(99), 
  year INTEGER,
  imdb_key VARCHAR(99) PRIMARY KEY
);

CREATE TABLE theaters (
  name VARCHAR(99) NOT NULL UNIQUE PRIMARY KEY,
  capacity INTEGER check (capacity > 0)
);

CREATE TABLE performances (
  name VARCHAR(99),
  perf_date DATE,
  perf_time TIME,
  imdb_key VARCHAR(99),
  PRIMARY KEY(name, perf_date, perf_time),
  FOREIGN KEY(name) REFERENCES theaters(name),
  FOREIGN KEY(imdb_key) REFERENCES movies(imdb_key)
);

CREATE TABLE tickets (
  ticket_id DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  user_id VARCHAR(99),
  name VARCHAR(99),
  perf_date DATE,
  perf_time TIME,
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(name, perf_date, perf_time) REFERENCES performances(name, perf_date, perf_time)
);
