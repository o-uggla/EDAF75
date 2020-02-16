import sqlite3


class Database(object):
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.c = self.conn.cursor()

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

    def performances(self):
        data = self.c.execute("SELECT * FROM performances").fetchall()
        return data

    def performances_by_key(self, performance_id):
        data = self.c.execute("SELECT * FROM movies WHERE performance_id = ?", [performance_id]).fetchall()
        return data

    def add_performance(self, imdbKey, theater, date, time):
        try:
            self.c.execute(
                """
                INSERT INTO performances(imdbKey, theater_name, perf_date, perf_time)
                VALUES (?, ?, ?, ?)
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

    def tickets(self):
        data = self.c.execute("SELECT * FROM tickets").fetchall()
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
