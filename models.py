import os
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False
database_path = os.getenv('DATABASE_URL')

print('current_db:', database_path)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def db_drop_and_create_all():
    """helper function used to drop current and create a fresh database"""
    db.drop_all()
    db.create_all()


def setup_db(app, database_path=database_path):
    """Configures primary application database"""
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    print('using db: ', app.config['SQLALCHEMY_DATABASE_URI'])
    db.app = app
    db.init_app(app)



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

    def __repr__(self):
        return f'<Actor id: "{self.id}", name: "{self.name}", age: "{self.age}", gender: "{self.gender}">'


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

    def __repr__(self):
        return f'<Movie id: "{self.id}", title: "{self.title}", year: "{self.year}">'
