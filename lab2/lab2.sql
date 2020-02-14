-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theater;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS performance;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS ticket;

PRAGMA foreign_keys=ON;

CREATE TABLE theater (
  t_name VARCHAR(99) NOT NULL UNIQUE,
  t_capacity INTEGER check (t_capacity > 0), 
  PRIMARY KEY(t_name)
);

CREATE TABLE movie (
  m_title VARCHAR(99), 
  m_year INTEGER,
  m_imdb_key VARCHAR(99),
  m_duration INTEGER,
  PRIMARY KEY(m_title, m_year)
);

CREATE TABLE performance (
  perf_date DATE,
  perf_time TIME,
  m_title VARCHAR(99),
  m_year INTEGER,
  t_name VARCHAR(99),
  PRIMARY KEY(t_name, perf_date, perf_time),
  FOREIGN KEY(m_title, m_year) REFERENCES movie(m_title, m_year),
  FOREIGN KEY(t_name) REFERENCES theater(t_name)
);

CREATE TABLE customer (
  username VARCHAR(99) NOT NULL UNIQUE,
  fullname VARCHAR(99),
  password INTEGER NOT NULL,
  PRIMARY KEY(username)
);

CREATE TABLE ticket (
  ticket_id DEFAULT (lower(hex(randomblob(16)))),
  username VARCHAR(99),
  t_name VARCHAR(99),
  perf_date DATE,
  perf_time TIME,
  PRIMARY KEY(ticket_id),
  FOREIGN KEY(username) REFERENCES customer(username),
  FOREIGN KEY(t_name, perf_date, perf_time) REFERENCES performance(t_name, perf_date, perf_time)
);
