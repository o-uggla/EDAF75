-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;

CREATE TABLE theaters (
  t_name VARCHAR(99) NOT NULL UNIQUE,
  t_capacity INTEGER check (t_capacity > 0), 
  PRIMARY KEY(t_name)
);

CREATE TABLE movies (
  m_title VARCHAR(99), 
  m_year INTEGER,
  m_imdb_key VARCHAR(99),
  m_duration INTEGER,
  PRIMARY KEY(m_title, m_year)
);

CREATE TABLE performances (
  perf_date DATE,
  perf_time TIME,
  m_title VARCHAR(99),
  m_year INTEGER,
  t_name VARCHAR(99),
  PRIMARY KEY(t_name, perf_date, perf_time),
  FOREIGN KEY(m_title, m_year) REFERENCES movies(m_title, m_year),
  FOREIGN KEY(t_name) REFERENCES theaters(t_name)
);

CREATE TABLE customers (
  username VARCHAR(99) NOT NULL UNIQUE,
  fullname VARCHAR(99),
  password INTEGER NOT NULL,
  PRIMARY KEY(username)
);

CREATE TABLE tickets (
  ticket_id DEFAULT (lower(hex(randomblob(16)))),
  username VARCHAR(99),
  t_name VARCHAR(99),
  perf_date DATE,
  perf_time TIME,
  PRIMARY KEY(ticket_id),
  FOREIGN KEY(username) REFERENCES customers(username),
  FOREIGN KEY(t_name, perf_date, perf_time) REFERENCES performances(t_name, perf_date, perf_time)
);
                               
-- Insert data into the tables.
INSERT
INTO    customers (username, fullname, password)
VALUES  ('silverswan131', 'Brad Gibson', 'firewall'),
        ('heavysnake217', 'Felix Andersen', 'trebor'),
        ('greenpeacock925', 'Carl Andersen', 'christia'),
        ('angrylion522', 'Sebastian Lozano', 'andy');

-- Insert data into the tables.
INSERT
INTO    theaters (t_name, t_capacity)
VALUES  ('Filmstaden Lund', 150),
        ('Rigoletto', 300),
        ('Lejonhufudet', 120),
        ('Filmstaden MOS', 550);
                               
-- Insert data into the tables.
INSERT
INTO    movies (m_title, m_year, m_imdb_key, m_duration)
VALUES  ('A Nightmare on Elm Street', 1984, 'tt0087800', 91),
        ('Awakening', 1990, 'tt0099077', 121),
        ('A League of Their Own' , 1992, 'tt0104694', 128),
        ('The Lord of the Rings: The Fellowship of the Ring', 2001, 'tt0120737', 178);
                               
-- Insert data into the tables.
INSERT
INTO    performances (perf_date, perf_time, m_title, m_year, t_name)
VALUES  ('2020-02-14', '11:00','Awakening', 1990,  'Rigoletto'),
        ('2020-02-14', '12:00','Awakening', 1990,  'Rigoletto'),
        ('2020-02-14', '13:00','Awakening', 1990,  'Rigoletto'),
        ('2020-02-14', '11:00','Awakening', 1990,  'Lejonhufudet'),
        ('2020-02-14', '12:00','Awakening', 1990,  'Lejonhufudet'),
        ('2020-02-14', '13:00','Awakening', 1990,  'Lejonhufudet'),
        ('2020-02-14', '13:00','Awakening', 1990,  'Filmstaden MOS'),
        ('2020-02-14', '14:00','Awakening', 1990,  'Filmstaden MOS'),
        ('2020-02-15', '16:00','Awakening', 1990,  'Filmstaden MOS');


