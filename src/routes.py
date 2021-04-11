from typing import List

from flask import request
from flask_restful import Resource

from src import api


class Smoke(Resource):
    def get(self):
        return {'message': 'OK'}, 200


def get_all_films() -> List[dict]:
    films = [
        {'id': f'{n}', 'title': f'Title {n}', 'release_date': f'{n}.04.2021'} for n in range(1, 11)
    ]
    return films


def get_film_by_uuid(uuid: str) -> dict:
    films = get_all_films()
    film = list(filter(lambda f: f['id'] == uuid, films))
    return film[0] if film else {}


def create_film(film_json: dict) -> List[dict]:
    films = get_all_films()
    films.append(film_json)
    return films


class FilmListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            films = get_all_films()
            return films, 200
        else:
            film = get_film_by_uuid(uuid)
            if not film:
                return '', 404
            else:
                return film, 200

    def post(self):
        film_json = request.json
        return create_film(film_json), 201

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


class ArtistsListApi(Resource):
    def get(self, uuid=None):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)