from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

from src import db
from src.database.models import Film
from src.resources.auth import token_required
from src.schemas.films import FilmSchema


class FilmListApi(Resource):
    schema = FilmSchema()

    @token_required
    def get(self, uuid=None):
        if not uuid:
            films = db.session.query(Film).options(
                joinedload(Film.actors)
            ).all()
            return self.schema.dump(films, many=True), 200

        film = db.session.query(Film).options(
            joinedload(Film.actors)
        ).filter_by(uuid=uuid).first()

        if not film:
            return '', 404
        else:
            return self.schema.dump(film), 200

    @token_required
    def post(self):
        try:
            film = self.schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.schema.dump(film), 201

    @token_required
    def put(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        try:
            film = self.schema.load(request.json, instance=film, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.schema.dump(film), 200

    @token_required
    def patch(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        try:
            film = self.schema.load(request.json, instance=film, session=db.session, partial=True)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.schema.dump(film), 200

    @token_required
    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return {'message': 'Deleted successfully'}, 204
