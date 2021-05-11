import datetime

from flask import request
from flask_restful import Resource

from src import api, db
from src.database.models import Film, Actor


class Smoke(Resource):
    def get(self):
        return {'message': 'OK'}, 200


class FilmListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            films = db.session.query(Film).all()
            return [f.to_dict() for f in films], 200
        else:
            film = db.session.query(Film).filter_by(uuid=uuid).first()
            if not film:
                return '', 404
            else:
                return film.to_dict(), 200

    def post(self):
        film_json = request.json
        if not film_json:
            return {'message': 'Wrong data'}, 400
        try:
            film = Film(
                title=film_json['title'],
                release_date=datetime.datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                distributed_by=film_json['distributed_by'],
                description=film_json.get('description'),
                length=film_json.get('length'),
                rating=film_json.get('rating')
            )
            db.session.add(film)
            db.session.commit()
        except(ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Create successfully'}, 201

    def put(self, uuid):
        film_json = request.json
        if not film_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Film).filter_by(uuid=uuid).update(
                dict(title=film_json['title'],
                     release_date=datetime.datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                     distributed_by=film_json['distributed_by'],
                     description=film_json.get('description'),
                     length=film_json.get('length'),
                     rating=film_json.get('rating')
                     )
            )
            db.session.commit()
        except(ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "", 404
        film_json = request.json
        title = film_json.get('title')
        release_date = datetime.datetime.strptime(film_json.get('release_date'), '%B %d, %Y') if film_json.get(
            'release_date') else None
        distributed_by = film_json.get('distributed_by')
        rating = film_json.get('rating')
        length = film_json.get('length')
        description = film_json.get('description')

        if title:
            film.title = title
        elif release_date:
            film.release_date = release_date
        elif distributed_by:
            film.distributed_by = distributed_by
        elif rating:
            film.rating = rating
        elif length:
            film.length = length
        elif description:
            film.description = description

        db.session.add(film)
        db.session.commit()
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return {'message': 'Deleted successfully'}, 204


class ActorListApi(Resource):
    def get(self, actor_id=None):
        if not actor_id:
            actors = db.session.query(Actor).all()
            return [a.to_dict() for a in actors], 200
        else:
            actor = db.session.query(Actor).filter_by(id=actor_id).first()
            if not actor:
                return '', 404
            else:
                return actor.to_dict(), 200

    def post(self):
        actor_json = request.json
        if not actor_json:
            return {'message': 'Wrong data'}, 400
        try:
            actor = Actor(
                name=actor_json['name'],
                surname=actor_json['surname'],
                age=actor_json['age']
            )
            db.session.add(actor)
            db.session.commit()
        except ValueError:
            return {'message': 'Wrong data'}, 400
        return {'message': 'Create successfully'}, 201

    def put(self, actor_id):
        actor_json = request.json
        if not actor_json:
            return {'message': 'Wrong data'}
        try:
            db.session.query(Actor).filter_by(id=actor_id).update(
                dict(
                    # todo: raise exception if id?
                    id=actor_json['id'],
                    name=actor_json['name'],
                    surname=actor_json['surname'],
                    age=actor_json['age']
                )
            )
            db.session.commit()
        except ValueError:
            return {'message': 'Wrong data'}, 400
        return {'message': 'Update successfully'}, 200

    def patch(self, actor_id):
        actor = db.session.query(Actor).filter_by(id=actor_id).first()
        if not actor:
            return "", 404
        actor_json = request.json
        # todo: raise exception?
        id = actor_json.get('id')
        name = actor_json.get('name')
        surname = actor_json.get('surname')
        age = actor_json.get('age') if actor_json.get else None

        if id:
            # todo: raise exception?
            actor.id = id
        elif name:
            actor.name = name
        elif surname:
            actor.surname = surname
        elif age:
            actor.age = age

        db.session.add(actor)
        db.session.commit()
        return {'message': 'Updated successfully'}

    def delete(self, actor_id):
        actor = db.session.query(Actor).filter_by(id=actor_id).first()
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return {'message': 'Deleted successfully'}, 204


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<actor_id>', strict_slashes=False)
