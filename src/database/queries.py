"""
SELECT QUERIES
"""

from src import db
from src.database import models


def all_films():
    print('\n', 'All films')

    films = db.session.query(models.Film).all()

    for f in films:
        print(f.rating, f)


def order_by_and_slice():
    print('', 'Order by and slice', 'rating.desc() - for descending order', sep='\n')

    ordered_films = db.session.query(models.Film).order_by(models.Film.rating)[:3]  # [:3]

    for f in ordered_films:
        print(f.rating, f)


def filter_and_filter_by():
    print('\n', 'Filter')

    filter_by_two_fields = db.session.query(models.Film).filter(
        models.Film.title != 'Harry Potter and Chamber of Secrets',
        models.Film.rating >= 7.9
    ).order_by(models.Film.rating).all()

    for f in filter_by_two_fields:
        print(f.rating, f)

    print('\n', 'Filter by', '')

    harry_potter_and_p_of_a = db.session.query(models.Film).filter_by(
        title='Harry Potter and the Prizoner of Azkaban'
    ).first()

    print(harry_potter_and_p_of_a)


def filter_by_text():
    print('\n', 'Filter by text( LIKE )', '')

    films = db.session.query(models.Film).filter(
        models.Film.title.like('%Deathly Hallows%')  # .ilike - case insensitive
    )
    for f in films:
        print(f)


def object_not_in():
    print('\n', 'object not in..', '')
    films = db.session.query(models.Film).filter(  # '~' - not, 'in_' - in
        ~models.Film.length.in_([146, 161])
    ).all()

    for f in films:
        print(f)


def querying_with_join():
    print('\n', 'JOIN, films with actors', '')
    films_with_actors = db.session.query(models.Film).join(models.Film.actors)[:2]

    for f in films_with_actors:
        print(f)


if __name__ == '__main__':
    all_films()
    order_by_and_slice()
    filter_and_filter_by()
    filter_by_text()
    object_not_in()
    querying_with_join()
