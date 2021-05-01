import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import db, Movie, Actor
from datetime import datetime


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        os.system('sh setup.sh')
        self.app = app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_TEST_PATH')
        # setup_db(self.app, self.database_path)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = self.app
        db.init_app(self.app)
        db.create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.actor = {
            'name': 'Leonardo Dicaprio',
            'age': '46',
            'gender': 'M'
        }

        self.updated_actor = {
            'name': 'Leonardo Dicaprio',
            'age': '47',
            'gender': 'M'
        }

        self.movie = {
            'title': 'Inception',
            'release_date': datetime.now()
        }

        self.updated_movie = {
            'title': 'Inception 2',
            'release_date': datetime.now()
        }

        self.director_headers = {'Content-Type': 'application/json',
                                 'Authorization': os.environ.get('DIRECTOR_TOKEN')}
        self.producer_headers = {'Content-Type': 'application/json',
                                 'Authorization': os.environ.get('PRODUCER_TOKEN')}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        """
        This function tests retrieving actors successfully.
        """
        res = self.client().get('/actors', headers=self.producer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        """
        This function tests retrieving movies successfully.
        """
        res = self.client().get('/movies', headers=self.producer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']))    
    
    def test_404_delete_unavailable_actor(self):
        """
        This function tests deleting an unavailable actor.
        """
        res = self.client().delete("/actors/999", headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_unavailable_movie(self):
        """
        This function tests deleting an unavailable movie.
        """
        res = self.client().delete("/movies/999", headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_add_actor(self):
        """
        This function tests inserting a new actor successfully.
        """
        res = self.client().post("/actors", json=self.actor, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_movie(self):
        """
        This function tests inserting a new movie successfully.
        """
        res = self.client().post("/movies", json=self.movie, headers=self.producer_headers)
        data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

    def test_400_add_actor(self):
        """
        This function tests inserting a actor with empty data.
        """
        # test empty data
        res = self.client().post("/actors", data=None, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')


    def test_400_add_movie(self):
        """
        This function tests inserting a movie with empty data.
        """
        res = self.client().post("/movies", data=None, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')

    def test_patch_actor(self):
        """
        This function tests updating an existing actor successfully.
        """
        res = self.client().patch("/actors/1", json=self.actor, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_patch_movie(self):
        """
        This function tests updating an existing movie successfully.
        """
        res = self.client().patch("/movies/2", json=self.movie, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor(self, actor_id=1):
        """
        This function tests deleting a spicific actor successfully
        """
        res = self.client().delete(f"/actors/{actor_id}", headers=self.producer_headers)
        data = json.loads(res.data)
        deleted_actor = Actor.query\
                            .filter(Actor.id == actor_id)\
                            .one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(deleted_actor)

    def test_delete_movie(self, movie_id=2):
        """
        This function tests deleting a spicific movie successfully
        """
        res = self.client().delete(f"/movies/{movie_id}", headers=self.producer_headers)
        data = json.loads(res.data)
        deleted_movie = Movie.query\
                            .filter(Movie.id == movie_id)\
                            .one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(deleted_movie)

    def test_404_patch_actor(self):
        """
        This function tests updating a non-existing actor successfully.
        """
        res = self.client().patch("/actors/999", json=self.actor, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_patch_movie(self):
        """
        This function tests updating a non-existing movie successfully.
        """
        res = self.client().patch("/movies/999", json=self.movie, headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_403_add_movie(self):
        """
        This function tests unauthorized insertion of a movie.
        """
        res = self.client().post("/movies", json={}, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message']['code'], 'unauthorized')
    
    def test_403_delete_movie(self):
        """
        This function tests unauthorized deletion of a movie.
        """
        res = self.client().delete("/movies/1", json={}, headers=self.director_headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message']['code'], 'unauthorized')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
