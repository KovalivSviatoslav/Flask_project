from src.resources.populate_db import PopulateDB, PopulateDBThreaded, PopulateDBThreadPoolExecutor
from src import api
from src.resources.actors import ActorListApi
from src.resources.auth import AuthRegister, AuthLogin

from src.resources.films import FilmListApi
from src.resources.smoke import Smoke
from src.resources.aggregations import AggregationApi

api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<pk>', strict_slashes=False)
api.add_resource(AggregationApi, '/aggregations', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(PopulateDB, '/populate-db', strict_slashes=False)
api.add_resource(PopulateDBThreaded, '/populate-db-threaded', strict_slashes=False)
api.add_resource(PopulateDBThreadPoolExecutor, '/populate-db-pool', strict_slashes=False)
