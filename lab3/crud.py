import sqlite3


class Database(object):
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)

    def users(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM users").fetchall()
        return data

    def movies(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM movies").fetchall()
        return data

    def theaters(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM theaters").fetchall()
        return data

    def performances(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM performances").fetchall()
        return data

    def tickets(self):
        c = self.conn.cursor()
        data = c.execute("SELECT * FROM tickets").fetchall()
        return data

    def reset(self):
        c = self.conn.cursor()

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

        c.execute("DELETE FROM users")
        c.executemany(
            "INSERT INTO users values (?,?,?)", users)

        c.execute("DELETE FROM movies")
        c.executemany(
            "INSERT INTO movies values (?,?,?)", movies)

        c.execute("DELETE FROM theaters")
        c.executemany(
            "INSERT INTO theaters values (?,?)", theaters)
        self.conn.commit()
