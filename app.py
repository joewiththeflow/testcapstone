import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


  @app.route("/movies")
  def get_movies():
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]

    return jsonify(
      {
        "movies": movies
      }
    )

  @app.route("/actors")
  def get_actors():
    selection = Actor.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in selection]

    return jsonify(
      {
        "actors": actors
      }
    )


  return app

  

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)