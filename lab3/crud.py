import sqlite3


class Database(object):
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = ON")

    def users(self):
        data = self.c.execute("SELECT * FROM users").fetchall()
        return data

    def movies(self, title: str = None, year: int = None):
        querryStr = "SELECT * FROM movies WHERE 1 = ?"
        querryArgs = (1, )

        if None != title:
            querryStr += " AND title = ? "
            querryArgs += (title, )
        if None != year:
            querryStr += " AND year = ? "
            querryArgs += (year, )

        data = self.c.execute(querryStr, querryArgs).fetchall()
        return data

    def movies_by_key(self, imdbKey):
        data = self.c.execute("SELECT * FROM movies WHERE imdbKey = ?", [imdbKey]).fetchall()
        return data

    def theaters(self):
        data = self.c.execute("SELECT * FROM theaters").fetchall()
        return data

    performanceQuerry = """
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
        """

    def performances(self):
        data = self.c.execute(Database.performanceQuerry).fetchall()
        return data

    def performances_by_key(self, performance_id):
        querryStr = Database.performanceQuerry + " WHERE performances.performance_id = ?"
        data = self.c.execute(querryStr, [performance_id]).fetchall()
        return data

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

        return data

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
