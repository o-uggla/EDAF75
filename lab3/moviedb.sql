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
  user_name VARCHAR(99),
  password INTEGER NOT NULL
);

CREATE TABLE movies (
  title VARCHAR(99), 
  year INTEGER,
  imdbKey VARCHAR(99) PRIMARY KEY
);

CREATE TABLE theaters (
  theater_name VARCHAR(99) NOT NULL UNIQUE PRIMARY KEY,
  capacity INTEGER check (capacity > 0)
);

CREATE TABLE performances (
  performance_id DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  theater_name VARCHAR(99),
  perf_date DATE,
  perf_time TIME,
  imdbKey VARCHAR(99),
  FOREIGN KEY(theater_name) REFERENCES theaters(theater_name),
  FOREIGN KEY(imdbKey) REFERENCES movies(imdbKey)
);

CREATE TABLE tickets (
  ticket_id DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  user_id VARCHAR(99),
  performance_id VARCHAR(16),
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(performance_id) REFERENCES performances(performance_id)
);
