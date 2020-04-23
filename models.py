from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import os

db = SQLAlchemy()

def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)



helper_table = db.Table(
    'helper_table',
    sa.Column(
        'actor_id',
        sa.Integer,
        sa.ForeignKey('actor.id'),
        primary_key=True
    ),
    sa.Column(
        'movie_id',
        sa.Integer,
        sa.ForeignKey('movie.id'),
        primary_key=True
    )
)

# Movie

class Movie(db.Model):
    __tablename__ = 'movie'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String())
    release_date = sa.Column(sa.DateTime())
    actors = db.relationship(
        'Actor',
        secondary=helper_table,
        backref=db.backref('movies', lazy='dynamic')
    )


    def info(self):
        actor_id_list = [item[0] for item in db.session.query(helper_table).filter(helper_table.c.movie_id==self.id).all()]
        if actor_id_list:
            cast = [Actor.query.get(i).name for i in actor_id_list]
        else:
            cast = 'Not Available'

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': cast
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Actor

class Actor(db.Model):
    __tablename__ = 'actor'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    age = sa.Column(sa.Integer)
    gender = sa.Column(sa.String(10))

    
    def info(self):
        movie_id_list = [item[1] for item in db.session.query(helper_table).filter(helper_table.c.actor_id==self.id).all()]
        if movie_id_list:
            in_movies = [Movie.query.get(i).title for i in movie_id_list]
        else:
            in_movies = []

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'seen_in_movies': in_movies
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()