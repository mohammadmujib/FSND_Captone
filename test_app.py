import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, helper_table


TEST_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/casting_agency'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2NmZGU0MzFhMGM4ZDY3MGNkMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MzUyMzcsImV4cCI6MTU4NzY0MjQzNywiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.uMc8zP3BOlOACrEdc4QOjyap3cksbfMvoBpcuRo1D4lejbKh9JQ4dcuTLyVKyGE0ZwLd6Je_xNKQMRDmJWpvxpxTT0rtccYY4aclxVp2xRZZVCPi0_LfFlgtcfURJI2SLqpqgIaYzxK6YyMYF154ZSpBw4qY1yMPGUCCOV1uX7BZxvoNYITAOe6C9_e9RiNiH39razypwHuLWzWgkSEr_IYSdyZnlL-g6HaAKaqOrVke8paPS1-VxIMW6fzjOzFzdXQfdbCsZcwu47oAQ_Fks96Da4mtG5yl95KmvduzDg9ialFfh7v1c4_c5H9KwwOZbKnXLv7m844GC_PLSrq14w'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2ZlZGU0MzFhMGM4ZDY3MGQyYiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MzU0NDIsImV4cCI6MTU4NzY0MjY0MiwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.sqoKnHAJ9nN8YS415O3MKl0KgfYRfxz_CvaPsm0TsRDisBfqTjWfiIxWIbdWaL0yvKkbvGq3EwEOVKCllbj-ppQ46kU4-cBELddDJMTrDRkDb_Q6zQUYo8U4RtKLgNSPksvzyIpiXtyBDY_O2oTZ_w0WcYyB8RvU1cLIEoRab4HTxAuaeG2Un2V4GIhLvbXeYztg4ifPjNHQghtlXpWJr_d1KohmjJXCmmf-5WDQzomLZVtE0ZtuXNtiU318wf-M08zDYLgBy4OErGQz-04Mi322ZngffPDaxILyUyCVZo809XRJbGAqX56Ze-DRDkWuP4RiFNHR11YDseAyCKqPEA'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhZDRhNjNmODAwMGM4YzIzNmJkZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MzU1MjEsImV4cCI6MTU4NzY0MjcyMSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.NcK6w6xpdjCIvfQ-8ladVaZI7oYjFpvv8jADOivpmmYxLsSP4uCPA3Ue_uxTrY2_39wHNmYTTGTHnBlK5Yd52C15nXQ1DnmBDxnyoEfG-GqN0I3kNnG5OwxSMpD2WQrwro5_OTeWGdj6jTleO37ZiHRSDrI2IvdtoIs3xklZKnrt_1zso3AsqCy1n00K99oAsVF-h0JSCJ5j3ds_XU9Qy0p5ImKE8jbPdnm-XhlyV98Mlwd6caV8qQHFthtJJVRRqM0hObdF0ila7lANXLRCrMnvLO4ZAf6mJsRZrkh9dm-H6Vn9hNWIkc0S050_GR7BD6nnD953Be2D5euTPP3khw'
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
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Brandon",
                                          "gender": "male",
                                          "age": 16
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_post_movies_by_executive_producer_with_auth_200(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "title": "Prestige",
                                          "release_date": "01/01/2005",
                                          'actors': [1]
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_movies_by_casting_assistant_without_auth_401(self):
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

    def test_get_actors_by_casting_assistant_without_auth_401(self):
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

    def test_get_movies_by_casting_assistant_without_auth_401(self):
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
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_patch_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
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

    def test_patch_movies_by_casting_assistant_without_auth_401(self):
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

    def test_delete_actors_by_casting_assistant_without_auth_401(self):
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

        def test_delete_movies_by_casting_assistant_without_auth_401(self):
            random_id = random.choice([movie.id for movie in Movie.query.all()])
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
