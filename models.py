
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
from sqlalchemy import Column, String, Integer, Date


Base = declarative_base()


DEBUG = True
SECRET_KEY = os.urandom(32)
#database_path = 'postgres://postgres:1234@localhost:5432/agency'
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



cast = db.Table(
    'cast',
    db.Column('actor_id', db.Integer,
              db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer,
              db.ForeignKey('movies.id'), primary_key=True),
)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

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
        }



class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    actors = db.relationship('Actor', secondary=cast,
                             backref=db.backref('movies', lazy=True))

    def __init__(self, title, year):
        self.title = title
        self.year = year

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
            'year': self.year
        }
