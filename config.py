import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    postgres_uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if postgres_uri.startswith("postgres://"):
        postgres_uri = postgres_uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = postgres_uri or 'sqlite:///' + str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some_secret_key'
