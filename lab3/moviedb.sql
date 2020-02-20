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
  user_name VARCHAR(99) NOT NULL,
  password VARCHAR(99) NOT NULL
);

CREATE TABLE movies (
  title VARCHAR(99) NOT NULL, 
  year INTEGER NOT NULL,
  imdbKey VARCHAR(99) PRIMARY KEY
);

CREATE TABLE theaters (
  theater_name VARCHAR(99) NOT NULL UNIQUE PRIMARY KEY,
  capacity INTEGER check (capacity > 0)
);

CREATE TABLE performances (
  performance_id TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  theater_name VARCHAR(99) NOT NULL,
  perf_date DATE,
  perf_time TIME,
  imdbKey VARCHAR(99) NOT NULL,
  FOREIGN KEY(theater_name) REFERENCES theaters(theater_name),
  FOREIGN KEY(imdbKey) REFERENCES movies(imdbKey)
);

CREATE TABLE tickets (
  ticket_id TEXT DEFAULT (lower(hex(randomblob(16)))) PRIMARY KEY,
  user_id VARCHAR(99) NOT NULL,
  performance_id VARCHAR(16) NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(performance_id) REFERENCES performances(performance_id)
);

DROP TRIGGER IF EXISTS check_tickets_availabillity;
CREATE TRIGGER check_tickets_availabillity
  BEFORE INSERT 
  ON tickets
BEGIN
  SELECT
    CASE WHEN
      (SELECT 
          theaters.capacity - coalesce(nbrTickets, 0) AS remainingSeats
        FROM performances
        LEFT JOIN theaters
        ON performances.theater_name = theaters.theater_name
        LEFT JOIN (
          SELECT performance_id, count() AS nbrTickets
          FROM tickets
          GROUP BY performance_id
        ) AS seats
        ON performances.performance_id = seats.performance_id
        WHERE performances.performance_id = NEW.performance_id) <= 0
    THEN
      RAISE (ROLLBACK, "No tickets left")
    END;
END;