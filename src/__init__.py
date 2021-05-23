import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app_config = app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask tutorial'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
app.debug = True


def sql_debug(response):
    queries = list(get_debug_queries())
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration

    print('=' * 80)
    print(f' SQL Queries - {len(queries)} in {round(total_duration * 1000, 2)}ms')
    print('=' * 80)

    return response


app.after_request(sql_debug)

from . import routes
from .database import models

# todo:
#  flask-film-api
#  run container at 5000 port:
#   docker run -p 5000:5000 films_api
#  check:
#  - flask blueprint
#  - SQLAlchemyAutoSchema: load_instance
#  - Config: SQLALCHEMY_TRACK_MODIFICATIONS
#  improve:
#  - add swagger for Actor and MtoM relation
