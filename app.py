import os
import json
from flask import Flask, request, abort, jsonify
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/')
    def index():
        return "<h1>Index page of Casting Agency Api!</h1>"

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE, OPTIONS'
        )
        return response

    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            movies = [movie.format() for movie in movies]
            for movie in movies:
                movie['actors'] = [i.format() for i in movie['actors']]
            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "movies": movies
            })
        except Exception:
            abort(422)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'status_code': 200,
                'status_message': 'OK',
                'actors': actors
            })
        except Exception as e:
            print(e)
            abort(422)


    @app.route('/movies/create', methods=['POST'])
    @requires_auth('post:movie')
    def post_new_movie():
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        new_movie = Movie.query.get(movie.id)
        new_movie = new_movie.format()

        return jsonify({
            'success': True,
            "status_code": 200,
            "status_message": 'OK',
            'created': movie.id,
            'new_movie': new_movie
        })

    @app.route('/actors/create', methods=['POST'])
    @requires_auth('post:actor')
    def post_new_actor():
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()
        new_actor = Actor.query.get(actor.id)
        new_actor = new_actor.format()

        return jsonify({
            'success': True,
            "status_code": 200,
            "status_message": 'OK',
            'created': actor.id,
            'new_actor': new_actor
        })

    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):
        target_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if target_movie is None:
            abort(404)
        target_movie.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": movie_id
                        })

    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id):
        targete_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if target_actor is None:
            abort(404)
        target_actor.delete()
        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": actor_id
                        })

    @app.route('/actors/patch/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(actor_id):

        actor = Actor.query.filter(Actor.id == actor_id)
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.movie_id = movie_id
        actor.update()
        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "message": "update occured"
        })

    @app.route('/movies/patch/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id)
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        movie.title = title
        movie.release_date = release_date
        movie.update()
        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "message": "update occured"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        })

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
