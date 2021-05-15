from flask_restful import Resource
from sqlalchemy import func

from src import db
from src.database.models import Film


class AggregationApi(Resource):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar()
        max_rating = db.session.query(func.max(Film.rating)).scalar()
        min_rating = db.session.query(func.min(Film.rating)).scalar()
        avg_rating = db.session.query(func.avg(Film.rating)).scalar()
        sum_length = db.session.query(func.sum(Film.length)).scalar()

        return {
            'films_count': films_count,
            'max_rating': max_rating,
            'min_rating': min_rating,
            'avg_rating': avg_rating,
            'sum_length': sum_length,
        }, 200
