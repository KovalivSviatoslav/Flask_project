import uuid

from src import db


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
    actors = db.relationship('Actor', secondary=films_actors, lazy='subquery', backref=db.backref('films', lazy=True))

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
        return f'Actor: {self.name} {self.surname}'
