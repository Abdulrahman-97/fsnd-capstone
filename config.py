import os
from decouple import config
SECRET_KEY = os.urandom(32)
USERNAME = config('USER')
KEY = config('KEY')
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
database_path = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{KEY}@127.0.0.1:5432/capstone'
if database_path:
    SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
