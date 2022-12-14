import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
#from settings import DB_NAME, DB_USER, DB_PASSWORD

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)
#database_path = 'postgresql://{}/{}'.format('localhost:5432', DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Movie Actors - Relationship Many-to-Many
"""
movie_actors = db.Table('movie_actors',
  db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
  db.Column('actor_id', db.Integer, db.ForeignKey('actors.id', ondelete='CASCADE'),primary_key=True)
)

"""
Movie

"""
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    actors = db.relationship('Actor', secondary=movie_actors, backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [
              {
              'id': actor.id,
              'name': actor.name
              }
              for actor in self.actors]
            }


"""
Actor

"""
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [
              {
              'id': movie.id,
              'name': movie.title
              }
              for movie in self.movies]
            }