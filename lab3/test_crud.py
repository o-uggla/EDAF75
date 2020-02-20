import unittest
from crud import Database

db = Database("movies.sqlite")

class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.reset()
        print("Base.setUp()")

    def tearDown(self):
        print("Base.tearDown()")

    def test_movies_by_key(self):
        data = [('The Shape of Water', 2017, 'tt5580390')]
        dbData = db.movies_by_key('tt5580390')
        self.assertEqual(data, dbData)

    def test_add_performance(self):
        success, dbData = db.add_performance('tt5580390', 'Kino', '2020-01-02', '19:00')
        self.assertTrue(success)
        performanceId = dbData.replace("/performances/","")
        data= [(performanceId, '2020-01-02', '19:00', 'The Shape of Water', 2017, 'Kino', 10)]
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
        performanceId = dbData.replace("/performances/","")
        success, dbData = db.add_ticket(performanceId, 'alice', 'dobido')
        self.assertTrue(success)
        success, dbData = db.add_ticket(performanceId, 'alice', 'dobido')
        self.assertTrue(success)

        data = [('2020-01-02', '19:00', 'Kino', 'The Shape of Water', 2017, 2)]
        dbData = db.customer_tickes('alice')
        self.assertEqual(data, dbData)

        data = []
        dbData = db.customer_tickes('bob')
        self.assertEqual(data, dbData)

        success, dbData = db.add_performance('tt4975722', 'Södran', '2020-01-03', '18:00')
        self.assertTrue(success)
        performanceId = dbData.replace("/performances/","")
        success, dbData = db.add_ticket(performanceId, 'alice', 'dobido')
        self.assertTrue(success)

        data = [('2020-01-02', '19:00', 'Kino', 'The Shape of Water', 2017, 2),
                ('2020-01-03', '18:00', 'Södran', 'Moonlight', 2016, 1)]
        dbData = db.customer_tickes('alice')
        self.assertEqual(sorted(data), sorted(dbData))



    def test_reset(self):
        users = [
            ('alice', 'Alice', 'dobido'),
            ('bob', 'Bob', 'whatsinaname')
        ]
        dbUsers = db.users()
        self.assertEqual(users, dbUsers)

        movies = [
            ('The Shape of Water', 2017, 'tt5580390'),
            ('Moonlight', 2016, 'tt4975722'),
            ('Spotlight', 2015, 'tt1895587'),
            ('Birdman', 2014, 'tt2562232')
        ]
        dbMovies = db.movies()
        self.assertEqual(movies, dbMovies)

        theaters = [
            ('Kino', 10),
            ('Södran', 16),
            ('Skandia', 100)
        ]
        dbTheaters = db.theaters()
        self.assertEqual(theaters, dbTheaters)

        performances = []
        dbPerformances= db.performances()
        self.assertEqual(performances, dbPerformances)

        tickets = []
        dbTickets= db.performances()
        self.assertEqual(tickets, dbTickets)

if __name__ == '__main__':
    unittest.main()