import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor
from sample_data import movies, actors, new_movie, new_actor, new_movie_non_existent_actor_id, new_actor_non_existent_movie_id, update_movie, update_actor, jwt
#from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        if self.database_path.startswith("postgres://"):
            self.database_path = self.database_path.replace("postgres://", "postgresql://", 1)
        #self.database_path = "postgresql://{}/{}".format('localhost:5432', DB_TEST_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
        # #########################################
        # # PREPOPULATE DATABASE WITH SAMPLE DATA IF EMPTY
        # # Uncomment and run app to insert sample data
        
        # # Add sample movies to db if empty
        # if not Movie.query.order_by(Movie.id).all():
        #   for movie in movies:
        #     movie.insert()

        # # Add sample actors to db if empty
        # if not Actor.query.order_by(Actor.id).all():
        #   for actor in actors:
        #     actor.insert()
        # #########################################

    
    def tearDown(self):
        """Executed after each test"""
        pass

    
    # GET MOVIES

    def test_get_movies(self):
        res = self.client().get("/movies", headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["movies"]))
    

    def test_405_put_movie_method_not_allowed(self):
        res = self.client().put("/movies", json={"id": 7, "title": "Star Wars: Episode 7 - The Force Awakens", "release_date": 2015}, headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "method not allowed")
    

    # GET ACTORS

    def test_get_actors(self):
        res = self.client().get("/actors", headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["actors"]))


    def test_405_put_actor_method_not_allowed(self):
        res = self.client().put("/actors", json={"id": 4, "name": "John Smith", "gender": "male"}, headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "method not allowed")



     # CREATE MOVIE

    def test_create_movie(self):
        res = self.client().post("/movies", json=new_movie.format(), headers=jwt)
        data = json.loads(res.data)
        
        # Get last movie in db
        movie = Movie.query.order_by(Movie.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["created"], movie.id)


    def test_422_create_movie_with_non_existent_actor_id(self):
        res = self.client().post("/movies", json=new_movie_non_existent_actor_id, headers=jwt)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



    # CREATE ACTOR

    def test_create_actor(self):
        res = self.client().post("/actors", json=new_actor.format(), headers=jwt)
        data = json.loads(res.data)
        
        # Get last movie in db
        actor = Actor.query.order_by(Actor.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["created"], actor.id)


    def test_422_create_actor_with_non_existent_movie_id(self):
        res = self.client().post("/actors", json=new_actor_non_existent_movie_id, headers=jwt)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    # UPDATE MOVIE

    def test_update_movie(self):
        res = self.client().patch("/movies/6", json=update_movie, headers=jwt)
        data = json.loads(res.data)
        
        movie_id = 6

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["movie"]["actors"][0]["id"], 4)
        self.assertEqual(data["movie"]["actors"][1]["id"], 5)
        self.assertEqual(data["movie"]["id"], movie_id)
        self.assertEqual(data["movie"]["release_date"], 1982)
        self.assertEqual(data["movie"]["title"], "Star Wars: Return of the Jediii")

    
    def test_405_put_specific_movie_method_not_allowed(self):
        res = self.client().put("/movies/6", json=update_actor, headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "method not allowed")


     # UPDATE ACTOR

    def test_update_actor(self):
        res = self.client().patch("/actors/5", json=update_actor, headers=jwt)
        data = json.loads(res.data)
        
        actor_id = 5

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor"]["movies"][0]["id"], 5)
        self.assertEqual(data["actor"]["movies"][0]["name"], "Star Wars: Episode 5 - The Empire Strikes Back")
        self.assertEqual(data["actor"]["id"], actor_id)
        self.assertEqual(data["actor"]["age"], 61)
        self.assertEqual(data["actor"]["gender"], "male")

    def test_405_put_specific_actor_method_not_allowed(self):
        res = self.client().put("/actors/5", json=update_movie, headers=jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "method not allowed")




   
    # # DELETE MOVIE

    # # Can only run this once successfully, then need to dropdb and recreate
    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/2', headers=jwt)
    #     data = json.loads(res.data)

    #     movie = Movie.query.filter(Movie.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertEqual(movie, None)
    

    # def test_422_movie_does_not_exist(self):
    #     res = self.client().delete("/movies/1000", headers=jwt)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")


    # # DELETE ACTOR

    # # Can only run this once successfully, then need to dropdb and recreate
    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/2', headers=jwt)
    #     data = json.loads(res.data)

    #     actor = Actor.query.filter(Actor.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertEqual(actor, None)
    

    # def test_422_actor_does_not_exist(self):
    #     res = self.client().delete("/actors/1000", headers=jwt)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")