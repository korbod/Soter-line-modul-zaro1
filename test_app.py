import unittest
import json
from app import app  # Feltételezve, hogy a Flask alkalmazás neve 'app'

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.debug = False  # Debug mód kikapcsolása
        self.app = app.test_client()

        # Tisztítjuk az adatbázist a teszt előtt
        self.clear_database()

    def tearDown(self):
        pass

    def clear_database(self):
        # Itt törölheted az adatbázis tartalmát vagy visszaállíthatod az eredeti állapotot
        pass

    def test_add_film(self):
        # Új film hozzáadása
        response = self.app.post('/add_film', data={
            'cim': 'Példa Film1',  # Teszt adat: Példa Film1
            'gyartasi_ev': '2020',
            'megtekintes_ev': '2020',
            'ertekeles': '8'
        }, follow_redirects=True)

        # Ellenőrizzük, hogy a válasz tartalmazza-e a "A film már létezik az adatbázisban!" üzenetet
        self.assertIn('A film már létezik az adatbázisban!', response.get_data(as_text=True))

    def test_statistics_rating(self):
        # Először hozzáadunk egy filmet
        self.app.post('/add_film', data={
            'cim': 'Példa Film',
            'gyartasi_ev': '2023',
            'megtekintes_ev': '2024',
            'ertekeles': '8'
        }, follow_redirects=True)
        
        # Majd lekérdezzük az értékelés alapján a statisztikát
        response = self.app.get('/statistics_rating?ertekeles=8')
        json_data = json.loads(response.data)
        
        # Ellenőrizzük, hogy a válasz tartalmazza-e a "Példa Film" címet
        found = False
        for film in json_data:
            if film['Cím'] == 'Példa Film':
                found = True
                break
        self.assertTrue(found, 'Példa Film not found in response')

    def test_statistics_year(self):
        # Először hozzáadunk egy filmet
        self.app.post('/add_film', data={
            'cim': 'Példa Film1',  # Teszt adat: Példa Film1
            'gyartasi_ev': '2020',
            'megtekintes_ev': '2020',
            'ertekeles': '8'
        }, follow_redirects=True)
        
        # Majd lekérdezzük az év alapján a statisztikát
        response = self.app.get('/statistics_year?evszam=2020')
        json_data = json.loads(response.data)
        
        # Ellenőrizzük, hogy a válasz tartalmazza-e a "Példa Film1" címet
        found = False
        for film in json_data:
            if film['Cím'] == 'Példa Film1':
                found = True
                break
        self.assertTrue(found, 'Példa Film1 not found in response')

if __name__ == '__main__':
    unittest.main()
