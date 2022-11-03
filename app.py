import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
from sample_data import movies, actors

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

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

  @app.route("/movies")
  @requires_auth('get:movies')
  def get_movies(jwt):
    selection = Movie.query.order_by(Movie.id).all()
    movies = [movie.format() for movie in selection]

    return jsonify(
      {
        "success": True,
        "movies": movies
      }
    )

  @app.route("/actors")
  @requires_auth('get:actors')
  def get_actors(jwt):
    selection = Actor.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in selection]

    return jsonify(
      {
        "success": True,
        "actors": actors
      }
    )

  # For movies we can allow the Executive Producer to add existing actors during movie creation
  # No other role can add movies
  # For this we need to ensure that actors actually exist if we try to add them to a movie
  # A Casting director can add Actors so we can allow that endpoint to add existing movies to actors
  @app.route("/movies", methods=["POST"])
  @requires_auth('post:movies')
  def create_movie(jwt):
      body = request.get_json()

      new_title = body.get("title", None)
      new_release_date = body.get("release_date", None)
      actors = body.get("actors", None)
      
      # TODO Some form of check regarding release_date
    
      try:
        new_movie = Movie(title=new_title, release_date=new_release_date)

        # Add existing actors to movie if included
        if actors:
          for id in actors:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor:
              new_movie.actors.append(actor)
            else:
              abort(422)

        new_movie.insert()
        
        return jsonify(
          {
              "success": True,
              "created": new_movie.id
          }
        )
      except:
        abort(422)


  @app.route("/actors", methods=["POST"])
  @requires_auth('post:actors')
  def create_actor(jwt):
      body = request.get_json()

      new_name = body.get("name", None)
      new_age = body.get("age", None)
      new_gender = body.get("gender", None)
      movies = body.get("movies", None)

      try:
        new_actor = Actor(name=new_name, age=new_age, gender=new_gender)

        # Add existing movies to actor if included
        if movies:
          for id in movies:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie:
              new_actor.movies.append(movie)
            else:
              abort(422)

        new_actor.insert()
        
        return jsonify(
          {
              "success": True,
              "created": new_actor.id
          }
        )
      except:
        abort(422)


  @app.route("/movies/<int:movie_id>", methods=["PATCH"])
  @requires_auth('patch:movies')
  def update_movie(jwt, movie_id):
      body = request.get_json()

      new_title = body.get("title", None)
      new_release_date = body.get("release_date", None)
      actors = body.get("actors", None)

      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          if movie is None:
            abort(404)

          if new_title:
            movie.title = new_title
          
          if new_release_date:
            movie.release_date = new_release_date

          if actors:
            # We should remove existing actors. Update must include all actors.
            movie.actors = []
            for id in actors:
              actor = Actor.query.filter(Actor.id == id).one_or_none()
              if actor:
                movie.actors.append(actor)
              else:
                abort(404)

          movie.update()

          return jsonify(
            {
                "success": True,
                "movie": movie.format()
            }
          )

      except:
          abort(400)


  @app.route("/actors/<int:actor_id>", methods=["PATCH"])
  @requires_auth('patch:actors')
  def update_actor(jwt, actor_id):
      body = request.get_json()

      new_name = body.get("name", None)
      new_age = body.get("age", None)
      new_gender = body.get("gender", None)
      movies = body.get("movies", None)

      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          if actor is None:
            abort(404)

          if new_name:
            actor.name = new_name
          
          if new_age:
            actor.age = new_age
          
          if new_gender:
            actor.gender = new_gender

          if movies:
            # We should remove existing movies. Update must include all movies.
            actor.movies = []
            for id in movies:
              movie = Movie.query.filter(Movie.id == id).one_or_none()
              if movie:
                actor.movies.append(movie)
              else:
                abort(404)

          actor.update()

          return jsonify(
            {
                "success": True,
                "actor": actor.format()
            }
          )

      except:
          abort(400)
  
  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

          if movie is None:
              abort(404)

          movie.delete()

          return jsonify(
              {
                  "success": True,
                  "deleted": movie_id
              }
          )

      except:
          abort(422)


  @app.route("/actors/<int:actor_id>", methods=["DELETE"])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

          if actor is None:
              abort(404)

          actor.delete()

          return jsonify(
              {
                  "success": True,
                  "deleted": actor_id
              }
          )

      except:
          abort(422)



  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "resource not found"}),
          404,
      )

  @app.errorhandler(405)
  def method_not_allowed(error):
      return (
          jsonify({"success": False, "error": 405, "message": "method not allowed"}),
          405,
      )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422,
      )

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


  @app.errorhandler(500)
  def server_error(error):
      return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500
  

  @app.errorhandler(AuthError)
  def not_authorised(error):
    return jsonify({
        "success": False, 
        "error": error.status_code, 
        "message": error.error['code'],
        "description": error.error['description']
        }), error.status_code

  return app





app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)