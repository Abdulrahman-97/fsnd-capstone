import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Movie, Actor
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object('config')
  db.init_app(app)
  migrate = Migrate(app, db)
  CORS(app)

  @app.route('/', methods=['GET'])
  def index():
    return "Welcome to Casting Agency API"

  
  '''
    Actors endpoints
  '''

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    '''
    This function handles requesting all available actors 
    Permission: get:actors
    '''
    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success': True,
      'actors': formatted_actors
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    '''
    This function handles inserting a new actor 
    Permission: post:actors
    '''
    try:
      name = request.get_json()['name']
      age = request.get_json()['age']
      gender = request.get_json()['gender']

      actor = Actor(name, age, gender)
      actor.insert()
    except:
      abort(400)


    return jsonify({
      'success': True
    })

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    '''
    This function handles deleting an existing actor. 
    Permission: delete:actors
    '''
    actor = Actor.query.get_or_404(actor_id)

    actor.delete()

    return jsonify({
      'success': True
    })
  
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    '''
    This function handles updating an existing actor. 
    Permission: patch:actors
    '''
    actor = Actor.query.get_or_404(actor_id)
    try:
      name = request.get_json()['name']
      age = request.get_json()['age']
      gender = request.get_json()['gender']

      actor.update(name, age, gender)
    except:
      abort(400)  
    return jsonify({
      'success': True,
      'actor': actor.format()
    })

    '''
    Movies endpoints
    '''

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    '''
    This function handles requesting all available movies 
    Permission: get:movies
    '''
    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      'success': True,
      'movies': formatted_movies
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    '''
    This function handles inserting a new movie 
    Permission: post:movies
    '''
    try:
      title = request.get_json()['title']
      release_date = request.get_json()['release_date']

      movie = Movie(title, release_date)
      movie.insert()
    except:
      abort(400)
    return jsonify({
      'success': True
    })

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    '''
    This function handles deleting an existing movie. 
    Permission: delete:movies
    '''
    movie = Movie.query.get_or_404(movie_id)

    movie.delete()

    return jsonify({
      'success': True
      })
  
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    '''
    This function handles updating an existing movie. 
    Permission: patch:movies
    '''
    movie = Movie.query.get_or_404(movie_id)
    
    try:
      title = request.get_json()['title']
      release_date = request.get_json()['release_date']
    except:
      abort(400)

    movie.update(title, release_date)
    
    return jsonify({
      'success': True,
      'movie': movie.format()
    })


  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422

  @app.errorhandler(400)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": "bad request"
                      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": "not found"
                      }), 404

  @app.errorhandler(AuthError)
  def unauthorized(AuthError):
      return jsonify({
                      "success": False, 
                      "error": AuthError.status_code,
                      "message": AuthError.error
                      }), AuthError.status_code



  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)