import sqlite3
import json 

class Database(object):
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = ON")

    def users(self):
        keys = ['user_id', 'user_name', 'password']
        data = self.c.execute("SELECT user_id, user_name, password FROM users").fetchall()
        res = self.prettierJsonList(keys, data)
        return res

    def movies(self, title: str = None, year: int = None):
        keys = ['imdbKey', 'title', 'year']
        querryStr = """
            SELECT imdbKey, title, year
            FROM movies
            WHERE 1 = ?
            """
        querryArgs = (1, )

        if None != title:
            querryStr += " AND title = ? "
            querryArgs += (title, )
        if None != year:
            querryStr += " AND year = ? "
            querryArgs += (year, )

        data = self.c.execute(querryStr, querryArgs).fetchall()
        res = self.prettierJsonList(keys, data)
        return res

    def movies_by_key(self, imdbKey):
        keys = ['imdbKey', 'title', 'year']
        data = self.c.execute(
            """
            SELECT imdbKey, title, year
            FROM movies
            WHERE imdbKey = ?
            """, [imdbKey]).fetchall()
        res = self.prettierJsonList(keys, data)
        return res

    def theaters(self):
        keys = ['theater', 'capacity']
        data = self.c.execute("SELECT theater_name, capacity FROM theaters").fetchall()
        res = self.prettierJsonList(keys, data)
        return res

    def performances(self):
        keys = ['performanceId', 'date', 'startTime', 'title', 'year', 'theater', 'remainingSeats']
        data = self.c.execute(
            """
            SELECT 
                performances.performance_id AS performanceId,
                perf_date AS date,
                perf_time AS startTime,
                title,
                year,
                performances.theater_name AS theater,
                theaters.capacity - coalesce(nbrTickets, 0) AS remainingSeats
            FROM performances
            LEFT JOIN movies
            ON performances.imdbKey = movies.imdbKey
            LEFT JOIN theaters
            ON performances.theater_name = theaters.theater_name
            LEFT JOIN (
                SELECT performance_id, count() AS nbrTickets
                FROM tickets
                GROUP BY performance_id
            ) AS seats
            ON performances.performance_id = seats.performance_id
            """).fetchall()
        return self.prettierJsonList(keys, data)

    def performances_by_key(self, performance_id):
        keys = ['performanceId', 'date', 'startTime', 'title', 'year', 'theater', 'remainingSeats']
        data = self.c.execute(
            """
            SELECT 
                performances.performance_id AS performanceId,
                perf_date AS date,
                perf_time AS startTime,
                title,
                year,
                performances.theater_name AS theater,
                theaters.capacity - coalesce(nbrTickets, 0) AS remainingSeats
            FROM performances
            LEFT JOIN movies
            ON performances.imdbKey = movies.imdbKey
            LEFT JOIN theaters
            ON performances.theater_name = theaters.theater_name
            LEFT JOIN (
                SELECT performance_id, count() AS nbrTickets
                FROM tickets
                GROUP BY performance_id
            ) AS seats
            ON performances.performance_id = seats.performance_id
            WHERE performances.performance_id = ?
            """, [performance_id]).fetchall()
        res = self.prettierJsonList(keys, data)
        return res

    def add_performance(self, imdbKey, theater, date, time):
        try:
            self.c.execute(
                """
                INSERT
                INTO performances(performance_id, imdbKey, theater_name, perf_date, perf_time)
                VALUES (lower(hex(randomblob(16))), ?, ?, ?, ?)
                """,
                (imdbKey, theater, date, time)
            )
            data = self.c.execute(
                """
                SELECT   performance_id
                FROM     performances
                WHERE    rowid = last_insert_rowid()
                """
            ).fetchone()
            self.conn.commit()
            return (True, ) + data
        except sqlite3.Error as e:
            print(e)
            return (False, None)
    
    def add_ticket(self, performance_id, user_id, password):
        try:
            data = self.c.execute(
                    """
                    SELECT   DISTINCT user_id
                    FROM     users
                    WHERE    user_id = ? AND password = ?
                    """, (user_id, password)
                ).fetchall()
            if 0 == len(data):
                return (False, 'Wrong password')

            self.c.execute(
                """
                INSERT
                INTO tickets (performance_id, user_id, ticket_id)
                VALUES (?, ?, lower(hex(randomblob(16))))
                """,
                (performance_id, user_id )
            )
            data = self.c.execute(
                    """
                    SELECT   ticket_id
                    FROM     tickets
                    WHERE    rowid = last_insert_rowid()
                    """
                ).fetchone()
            self.conn.commit()
            return (True, ) + data
        except sqlite3.Error as e:
            if 'No tickets left' == e.args[0]:
                return (False, 'No tickets left')
            return(False, 'Error')

    def customer_tickes(self, user_id):
        keys = ['performanceId', 'date', 'startTime', 'title', 'year', 'theater', 'remainingSeats']
        data = self.c.execute(
            """
            SELECT
                performances.performance_id,
                perf_date,
                perf_time,
                title,
                year,
                theater_name,
                count()
            FROM     tickets
            LEFT JOIN performances
            ON performances.performance_id = tickets.performance_id
            LEFT JOIN movies
            ON movies.imdbKey = performances.imdbKey
            WHERE    user_id = ?
            GROUP BY tickets.performance_id
            """, [user_id]
            ).fetchall()
        res = self.prettierJsonList(keys, data)
        return res
        
    def reset(self):
        users = [
            ('alice', 'Alice', 'dobido'),
            ('bob', 'Bob', 'whatsinaname')
        ]

        movies = [
            ('The Shape of Water', '2017', 'tt5580390'),
            ('Moonlight', '2016', 'tt4975722'),
            ('Spotlight', '2015', 'tt1895587'),
            ('Birdman', '2014', 'tt2562232')
        ]

        theaters = [
            ('Kino', '10'),
            ('Södran', '16'),
            ('Skandia', '100')
        ]
        self.c.execute("DELETE FROM tickets")
        self.c.execute("DELETE FROM performances")

        self.c.execute("DELETE FROM users")
        self.c.executemany(
            "INSERT INTO users values (?,?,?)", users)

        self.c.execute("DELETE FROM movies")
        self.c.executemany(
            "INSERT INTO movies values (?,?,?)", movies)

        self.c.execute("DELETE FROM theaters")
        self.c.executemany(
            "INSERT INTO theaters values (?,?)", theaters)
        self.conn.commit()

    def prettierJsonList(self, key, data):
        return [dict(zip(key, d))for d in data]
