from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

from src import db
from src.database.models import Actor
from src.resources.auth import token_required
from src.schemas.actors import ActorSchema


class ActorListApi(Resource):
    schema = ActorSchema()

    @token_required
    def get(self, pk=None):
        if not pk:
            actors = db.session.query(Actor).options(
                joinedload(Actor.films)
            ).all()
            return self.schema.dump(actors, many=True), 200

        actor = db.session.query(Actor).options(
                joinedload(Actor.films)
            ).filter_by(id=pk).first()

        if not actor:
            return '', 404
        else:
            return self.schema.dump(actor), 200

    @token_required
    def post(self):
        try:
            film = self.schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {'message': str(err)}, 400
        return self.schema.dump(film), 201

    @token_required
    def put(self, pk):
        film = db.session.query(Actor).filter_by(id=pk)
        if not film:
            return '', 404
        try:
            film = self.schema.load(request.json, session=db.session)
        except ValidationError as err:
            return {'messages': str(err)}, 400
        db.session.add(film)
        db.session.commit()
        return self.schema.dump(film), 200

    @token_required
    def patch(self, pk):
        actor = db.session.query(Actor).filter_by(id=pk).first()
        if not actor:
            return '', 400
        try:
            actor = self.schema.load(request.json, instance=actor, session=db.session, partial=True)
        except ValidationError as err:
            return {'message': str(err)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.schema.dump(actor), 200

    @token_required
    def delete(self, pk):
        actor = db.session.query(Actor).filter_by(id=pk).first()
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return {'message': 'Deleted successfully'}, 204
