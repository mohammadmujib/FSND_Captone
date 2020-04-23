import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, helper_table


TEST_DATABASE_URI = 'postgresql://postgres:puru2000@localhost/casting_agency'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2NmZGU0MzFhMGM4ZDY3MGNkMiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjQ2NzMsImV4cCI6MTU4NzYzMTg3MywiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.aT9rJiJjmHP_tzg5d2mPQLLV0pu17SvN_Q34E-IDoIh5_c4mEe9-ngRpJsahrEkvAuyECtsyeS97Po16axT3OfpDhetrjAwefM1-bnBXFhcWHwr35fXC5xzUWQYJbDtXcgmTMDu6tC_om4v4MiaB1ug-XaR7s7iY0rAJqOnFr_mEL_1eB378fjQFU1ga7I11iUqpmgs6-4L_spH6I3TsJrD41HQM4vqwFJURjy0igZa124P5eg-XbhRfGbDQqnZ2_2KphYwG3At2EPkxX8QI0bcNEFWclar50SusV_PJuABxX7SAOpIuwKBPRFmpw9zN6JKPNVbCkAU1vuWoy9Mr9A'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhY2ZlZGU0MzFhMGM4ZDY3MGQyYiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjQ0NTUsImV4cCI6MTU4NzYzMTY1NSwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.KMnRevs3CvlyInd-3lyy-O2puQwmld_NtzIl0L0x_zfGd2KbApN5MthUlZtedHBKA_EElQuKcuOd5RFL2FOaggUspnDE1ms8oCjauTMd5NIEbs1DOmLjpceEsyV_baeeqH7BmBrH3_1__OlTg98dX5dN-si1ppNf4MjhaYtN57DGd1dFQ5AyW7B6E0si_7jjgq3Q70WlCgM0BrXY6_2ehOhI8KbHMox-3QZTp3W_4zavmmHeUUWTNgQMz8gdhAko8gHV25ADHUhqdGXN7a6VN0Mg4u-tZZATmyDd7tY3p5z0BNs19iNs2RQ1cKOsF-RZmKvc7T_F3becgs_62UlJvg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpR3IwQW5XV3k2Y2tNZWM5Qlk1diJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWNhc3RpbmcuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWNhZDRhNjNmODAwMGM4YzIzNmJkZCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODc2MjE3MTYsImV4cCI6MTU4NzYyODkxNiwiYXpwIjoiMVdPVHhjTDlCSTJNWTdiRjNwb1A4YmZUV2g2bzRabk4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.hG06TJBpR2hLa8RjKIhu78-00AC-H0AzmvXgBooi3xtmvKuEQR33dMtzRK24yk9VExeXlYAOgmHp8trrHU8uy9iQqO3R9Tv4PnZZMYDeUrAWescZVZokSRNUTHLH7GNcrBSn-N2w8CUWkhYzFVkYm9iNIUkmxpIzk0VFOMV-_9zCvNdw9ongs-PHi0hxNX3ywPixVLQ2jtRXsDELA5swY1Gpvy-2VfQ-RwOwMlgFc_BOg9UQ75U38EFqRC1H8MMVUUJGP31L6pqREEBYaXTl4bujqleoKJysazZqG6FwdZKQdLZCdx11ATBLLiqJp3vWxMZuC3SuHC-XdlQuvh_9Xg'

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