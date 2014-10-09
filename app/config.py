# config.py

import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flastaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = 'TRUE'
SECRET_KEY = 'my_precious'

DATABASE_PATH = os.path.join(basedir, DATABASE)