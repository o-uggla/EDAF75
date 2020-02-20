import unittest
from crud import Database

db = Database("movies.sqlite")

class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.reset()
        print("Base.setUp()")

    def test_movies_by_key(self):
        keys = ['imdbKey', 'title', 'year']
        data = [('tt5580390', 'The Shape of Water', 2017)]
        dbData = db.movies_by_key('tt5580390')
        res = db.prettierJsonList(keys, data)
        self.assertEqual(sorted(res), sorted(dbData))

    def test_add_performance(self):
        keys = ['performanceId', 'date', 'startTime', 'title', 'year', 'theater', 'remainingSeats']
        success, dbData = db.add_performance('tt5580390', 'Kino', '2020-01-02', '19:00')
        self.assertTrue(success)
        performanceId = dbData.replace("/performances/","")

        data = [(performanceId, '2020-01-02', '19:00', 'The Shape of Water', 2017, 'Kino', 10)]
        data = db.prettierJsonList(keys, data)
        dbData = db.performances_by_key(performanceId)
        self.assertEqual(data, dbData)

        success, dbData = db.add_performance('tt5580390', 'Non-existing-theater', '2020-01-02', '19:00')
        self.assertFalse(success)
        dbData = db.performances()
        self.assertEqual(len(dbData), 1)
    
    def text_performances(self):
        pass

    def test_add_ticket(self):
        success, dbData = db.add_performance('tt5580390', 'Kino', '2020-01-02', '19:00')
        self.assertTrue(success)
        performanceId = dbData.replace("/performances/","")
        success, dbData = db.add_ticket(performanceId, 'alice', 'dobido')
        self.assertTrue(success)

        success, dbData = db.add_ticket(performanceId, 'alice', '')
        data = 'Wrong password'

        self.assertFalse(success)
        self.assertEqual(data, dbData)

        for i in range(9):
            success, dbData = db.add_ticket(performanceId, 'bob', 'whatsinaname')
            self.assertTrue(success)

        success, dbData = db.add_ticket(performanceId, 'alice', 'dobido')
        data = 'No tickets left'
        self.assertFalse(success)
        self.assertEqual(data, dbData)

        success, dbData = db.add_ticket('', 'alice', 'dobido')
        data = 'Error'
        self.assertFalse(success)
        self.assertEqual(data, dbData)

    def test_customer_tickets(self):
        success, dbData = db.add_performance('tt5580390', 'Kino', '2020-01-02', '19:00')
        self.assertTrue(success)
        performanceId1 = dbData.replace("/performances/","")
        success, dbData = db.add_ticket(performanceId1, 'alice', 'dobido')
        self.assertTrue(success)
        success, dbData = db.add_ticket(performanceId1, 'alice', 'dobido')
        self.assertTrue(success)

        # Test show tickets to one show
        keys = ['performanceId', 'date', 'startTime', 'title', 'year', 'theater', 'remainingSeats']
        data = [(performanceId1, '2020-01-02', '19:00', 'The Shape of Water', 2017, 'Kino', 2)]
        data = db.prettierJsonList(keys, data)
        data.sort(key=lambda x: x['performanceId'], reverse=False)
        dbData = db.customer_tickes('alice')
        dbData.sort(key=lambda x: x['performanceId'], reverse=False)
        for d, dbD in zip(data, dbData):
            self.assertDictEqual(d, dbD)

        # Test user got no tickets
        data = []
        dbData = db.customer_tickes('bob')
        self.assertEqual(data, dbData)

        # Test show tickets to multiple shows
        success, dbData = db.add_performance('tt4975722', 'Södran', '2020-01-03', '18:00')
        self.assertTrue(success)
        performanceId2 = dbData.replace("/performances/","")
        success, dbData = db.add_ticket(performanceId2, 'alice', 'dobido')
        self.assertTrue(success)

        data = [(performanceId2, '2020-01-03', '18:00', 'Moonlight', 2016, 'Södran', 1),
                (performanceId1, '2020-01-02', '19:00', 'The Shape of Water', 2017, 'Kino', 2)]
        data = db.prettierJsonList(keys, data)
        data.sort(key=lambda x: x['performanceId'], reverse=False)
        dbData = db.customer_tickes('alice')
        dbData.sort(key=lambda x: x['performanceId'], reverse=False)
        for d, dbD in zip(data, dbData):
            self.assertDictEqual(d, dbD)

    def test_reset(self):
        keys = ['user_id', 'user_name', 'password']
        users = [
            ('alice', 'Alice', 'dobido'),
            ('bob', 'Bob', 'whatsinaname')
        ]
        users = db.prettierJsonList(keys, users)
        dbUsers = db.users()
        for user, dbUser in zip(users, dbUsers):
            self.assertDictEqual(user, dbUser)

        keys = ['title', 'year', 'imdbKey']
        movies = [
            ('The Shape of Water', 2017, 'tt5580390'),
            ('Moonlight', 2016, 'tt4975722'),
            ('Spotlight', 2015, 'tt1895587'),
            ('Birdman', 2014, 'tt2562232')
        ]
        movies = db.prettierJsonList(keys, movies)
        dbMovies = db.movies()
        for movie, dbMovie in zip(movies, dbMovies):
            self.assertDictEqual(movie, dbMovie)

        keys = ['theater', 'capacity']
        theaters = [
            ('Kino', 10),
            ('Södran', 16),
            ('Skandia', 100)
        ]
        theaters = db.prettierJsonList(keys, theaters)
        dbTheaters = db.theaters()
        for theater, dbTheater in zip(theaters, dbTheaters):
            self.assertDictEqual(theater, dbTheater)

        performances = []
        dbPerformances= db.performances()
        self.assertEqual(performances, dbPerformances)

        tickets = []
        dbTickets= db.performances()
        self.assertEqual(tickets, dbTickets)

if __name__ == '__main__':
    unittest.main()