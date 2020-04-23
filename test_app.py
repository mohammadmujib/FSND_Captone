import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db
from dotenv import load_dotenv

load_dotenv()

test_database_path = 'postgresql://postgres:1234@localhost:5432/castings_test'

bearer_tokens = {
    "casting_assistant": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2NmZGU0MzFhMGM4ZDY3MGNkMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjQ2NzMsImV4cCI6MTU4NzYzMTg3MywiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.aT9rJiJjmHP_tzg5d2mPQLLV0pu17SvN_Q34E-IDoIh5_c4mEe9-ngRpJsahrEkvAuyECtsyeS97Po16axT3OfpDhetrjAwefM1-bnBXFhcWHwr35fXC5xzUWQYJbDtXcgmTMDu6tC_om4v4MiaB1ug-XaR7s7iY0rAJqOnFr_mEL_1eB378fjQFU1ga7I11iUqpmgs6-4L_spH6I3TsJrD41HQM4vqwFJURjy0igZa124P5eg-XbhRfGbDQqnZ2_2KphYwG3At2EPkxX8QI0bcNEFWclar50SusV_PJuABxX7SAOpIuwKBPRFmpw9zN6JKPNVbCkAU1vuWoy9Mr9A",
    "executive_producer": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhZDRhNjNmODAwMGM4YzIzNmJkZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjE3MTYsImV4cCI6MTU4NzYyODkxNiwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.hG06TJBpR2hLa8RjKIhu78-00AC-H0AzmvXgBooi3xtmvKuEQR33dMtzRK24yk9VExeXlYAOgmHp8trrHU8uy9iQqO3R9Tv4PnZZMYDeUrAWescZVZokSRNUTHLH7GNcrBSn-N2w8CUWkhYzFVkYm9iNIUkmxpIzk0VFOMV-_9zCvNdw9ongs-PHi0hxNX3ywPixVLQ2jtRXsDELA5swY1Gpvy-2VfQ-RwOwMlgFc_BOg9UQ75U38EFqRC1H8MMVUUJGP31L6pqREEBYaXTl4bujqleoKJysazZqG6FwdZKQdLZCdx11ATBLLiqJp3vWxMZuC3SuHC-XdlQuvh_9Xg",
    "casting_director": "Bearer access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2ZlZGU0MzFhMGM4ZDY3MGQyYiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjQ0NTUsImV4cCI6MTU4NzYzMTY1NSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.KMnRevs3CvlyInd-3lyy-O2puQwmld_NtzIl0L0x_zfGd2KbApN5MthUlZtedHBKA_EElQuKcuOd5RFL2FOaggUspnDE1ms8oCjauTMd5NIEbs1DOmLjpceEsyV_baeeqH7BmBrH3_1__OlTg98dX5dN-si1ppNf4MjhaYtN57DGd1dFQ5AyW7B6E0si_7jjgq3Q70WlCgM0BrXY6_2ehOhI8KbHMox-3QZTp3W_4zavmmHeUUWTNgQMz8gdhAko8gHV25ADHUhqdGXN7a6VN0Mg4u-tZZATmyDd7tY3p5z0BNs19iNs2RQ1cKOsF-RZmKvc7T_F3becgs_62UlJvg"
}

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}

class CastingAgencyTestCase(unittest.TestCase):

    def insert_data(self):
        """Seed test database with initial data"""
        actor1 = Actor(name="NIck JOnas", age=25, gender='m')
        actor2 = Actor(name="rock", age=22, gender='f')
        actor3 = Actor(name="Salman", age=32, gender='f')

        movie1 = Movie(title="Joker", release_date="02/01/2000")
        movie2 = Movie(title="Titanic", release_date="05/07/2015")
        movie3 = Movie(title="abcd", release_date="09/11/2029")

        self.db.session.add(actor1)
        self.db.session.add(actor2)
        self.db.session.add(actor3)

        self.db.session.add(movie1)
        self.db.session.add(movie2)
        self.db.session.add(movie3)
        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        setup_db(self.app, database_path=test_database_path)
        with self.app.app_context():
            self.db = db

            self.db.drop_all()
            self.db.create_all()

            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()
        pass
    
#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#

    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            "name": "Crisso",
            "gender": "m",
            "age": 25
        }

        res = self.client().post('/actors', json=json_create_actor,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name': 'Crisso',
            'age': 25
        }

        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#
    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_get_all_actors(self):

        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#
    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/2', json=json_edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_404_edit_actor(self):
        """Test PATCH with non json body"""

        res = self.client().patch('/actors/123412', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/15125', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#

    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title': 'Crisso Movie',
            'release_date': "02/07/2020"
        }

        res = self.client().post('/movies', json=json_create_movie,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_401_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_date': "02/07/2020"
        }

        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')
#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        json_edit_movie = {
            "title":"fast and furious"
        }
        res = self.client().patch('/movies/1', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_date': "02/03/2020"
        }
        res = self.client().patch('/movies/123412', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
    
