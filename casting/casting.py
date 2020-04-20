
from flask import Flask, request, abort, jsonify, Blueprint
from flask_cors import CORS

from models import setup_db, Movie, Actor

from auth.auth import requires_auth

casting = Blueprint('casting', __name__)



@casting.route('/movies')
@requires_auth('get:movies')
def get_movies(token):
    movies = Movie.query.order_by(Movie.id).all()
    if movies == []:
        abort(404)
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
        "success": True,
        "movies": formatted_movies
    })

@casting.route('/movies', methods=["POST"])
@requires_auth('post:movies')
def create_movie(token):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)
    new_actors = Actor.query.filter(Actor.id.in_(
        body.get('actors', None))).all()

    try:
        movie = Movie(title=new_title,
                      release_date=new_release_date
                      )
        movie.actors = new_actors
        movie.insert()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })
    except Exception:
        abort(422)

@casting.route('/movies/<int:movie_id>', methods=["PATCH"])
@requires_auth('patch:movies')
def edit_movie(token, movie_id):
    body = request.get_json()

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    try:
        movie.title = body.get('title', None)
        movie.release_date = body.get('release_date', None)
        movie.actors = Actor.query.filter(Actor.id.in_(
            body.get('actors', None))).all()
        movie.update()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })
    except Exception:
        abort(422)

@casting.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth('delete:movies')
def delete_movie(token, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    try:
        movie.delete()
        movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })
    except Exception:
        abort(422)

@casting.route('/actors')
@requires_auth('get:actors')
def get_actors(token):
    actors = Actor.query.order_by(Actor.id).all()
    if actors == []:
        abort(404)
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
        "success": True,
        "actors": formatted_actors
    })

@casting.route('/actors', methods=["POST"])
@requires_auth('post:actors')
def create_actor(token):
    body = request.get_json()

    new_name = body.get('name', None)
    new_gender = body.get('gender', None)
    new_age = body.get('age', None)

    try:
        actor = Actor(name=new_name,
                      gender=new_gender, age=new_age)
        actor.insert()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })
    except Exception:
        abort(422)

@casting.route('/actors/<int:actor_id>', methods=["PATCH"])
@requires_auth('patch:actors')
def edit_actor(token, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()

    try:
        actor.name = body.get('name', None)
        actor.gender = body.get('gender', None)
        actor.age = body.get('age', None)
        actor.update()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })
    except Exception:
        abort(422)

@casting.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth('delete:actors')
def delete_actor(token, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })
    except Exception:
        abort(422)
