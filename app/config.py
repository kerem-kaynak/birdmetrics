from os import environ
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL').replace("://", "ql://", 1)
SQLALCHEMY_TRACK_MODIFICATIONS = False