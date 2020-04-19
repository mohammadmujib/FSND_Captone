import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


# TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
# CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
# CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
# EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')

TEST_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/agency'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2NmZGU0MzFhMGM4ZDY3MGNkMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczMjY1NzksImV4cCI6MTU4NzMzMzc3OSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.oQCC_nYpgx-zjIhVoHCKtFPjbQDuuhcAPfvRCr1x1Rah5UjXlUmCf67g7glkjJ_t4kPc7NM77YFlgQqY3AlgEmz16ohXoDk1N4v52CFFTUbddz3MBBtLl20DFDictsl6VQm8HsCcaH58iG9HvglHy_rbXlvZeFuQflTRmRDSxVyKHBbeMFMVUfbsdQl1WuhwAXbEZkYdDWTk4haTyRkqNSmx7cEvh8iEPlW3rRRYOikSoKk4tkp63x3OFqGi08NNK4KYvHWgznmF_-3JdruLlaTpkKNkOpQx_0TmN2lsARTxuqjethqYVv0ExXE_xXtfKs2Z7avru7ZzvfgYof0PuA'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2ZlZGU0MzFhMGM4ZDY3MGQyYiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczMjY2NzUsImV4cCI6MTU4NzMzMzg3NSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsInBvc3Q6YWN0b3IiXX0.F1PkfwmFb0fPPrcU78Q5VkTsiWHZWsuxKgEqYYzhoBAuCLhOQnuV1Li_KSy6GsTw8aG6RxyyyICMqlSapw34XtShI2y6ZUSoZ7wFqYCX5vOzsDk9FqBgiXXF5pQYNho7b6xrCMR72LnzvI5haF6XVIfdGpilwKXruUWaXgepSmt2BpHED4p1chDC_x9S1GWYYkMej7rFuz3wke5jJg6F93SO5_uLDrwM85_k5EKImKsDFW2ihlhGK3L4d9tkwCO9HBBu5yLCJWcGMeK-fOPmeQKmqFLgPxb23ZiWAD7DQV__YYFTKCUKsZm-JcIZ6R1zxPt_C7nnWHzhuXHKvfU5IA'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhZDRhNjNmODAwMGM4YzIzNmJkZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODczMjY3OTgsImV4cCI6MTU4NzMzMzk5OCwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.CL6LJJGLwFZkrHNPjpBO26GQw7qzpbnk7q-F19NLWtru5T9n35O7JhGnb9QfATbxnOW1sDMNCHzIMaT_GJVOMdFSwxoRxrA8z-ZBJG8gd1WnYuZTr12IVCooQ5nOj1U3Gd82mC2RQKOkYCGqFUYkJ7532V3rN-an9GlpLAwRjuWHSvSqo7Gsz0Y1_GpmtPXEhdgDclBYj-oMZD2dSG18a63XrOY_Mc82x1gAej__EwaGJQubI0An8WCoZE_luCTlohaHrF9IxtgKnCx6F5KdbSMd29w49CoJM_2fS71vOA1ldOunvasmLNfJ7KCKmP-5po_KodK0sTwYAJl6A4GILA'


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = CASTING_ASSISTANT
        self.casting_director = CASTING_DIRECTOR
        self.executive_producer = EXECUTIVE_PRODUCER
        setup_db(self.app)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    '''
    RBAC TEST
    '''

    def test_post_movies_by_executive_producer(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "title": "Blade Runner",
                                          "release_date": "01/01/2017",
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_post_movies_by_casting_assistant(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "title": "American Made",
                                          "release_date": "05/12/2018",
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_post_actors_by_executive_producer_with_auth_200(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "name": "Alex",
                                          "gender": "male",
                                          "age": 25,
                                          "movie_id": 1
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_post_actors_by_casting_assistant(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Brandon",
                                          "gender": "male",
                                          "age": 16,
                                          "movie_id": 3
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_get_actors_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_get_actors_by_casting_assistant(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_get_movies_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_get_movies_by_casting_assistant(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_patch_actors_by_casting_director_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10,
            "movie_id": 1
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_patch_actors_by_casting_assistant(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10,
            "movie_id": 1
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_patch_movies_by_casting_director_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_patch_movies_by_casting_assistant(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def failed_test_delete_actors_by_casting_assistant(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def failed_test_delete_movies_by_casting_assistant(self):
        random_id = random.choice(
            [movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')


if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
