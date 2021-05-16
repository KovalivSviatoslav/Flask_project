import uuid

from werkzeug.security import generate_password_hash

from src import db


# =========================================================
# db.relationship( lazy='subquery'(automatically load the related data) / True (load object if ))
# in backref=db.backref(lazy=True) is the same
#
# If we need to load related data manually, use this in your queries:
# options(joinedload/selectinload(<model>.related_field))
# selectinload(<model.field>) - will make a subquery
# =========================================================

films_actors = db.Table(
    'films_actors',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('films.id'), primary_key=True)
)


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, index=True, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.String(120), nullable=False)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)
    actors = db.relationship('Actor', secondary=films_actors, lazy=True, backref=db.backref('films', lazy=True))

    def __init__(self, title, release_date, description, distributed_by, length, rating, actors=None):
        # we use this because of have uuid field
        self.title = title
        self.release_date = release_date
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        self.uuid = str(uuid.uuid4())
        if actors:
            self.actors = actors
        else:
            self.actors = []

    def __repr__(self):
        return f'Film({self.title}, {self.uuid}, {self.distributed_by}, {self.release_date}, {self.actors})'


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Actor({self.name}, {self.surname}, {self.age}, {self.is_active})'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.id_admin = is_admin
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.uuid})'
