import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
database_path = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PATH')
if database_path:
    SQLALCHEMY_DATABASE_URI = database_path.replace('postgres', 'postgresql')
SQLALCHEMY_TRACK_MODIFICATIONS = False
