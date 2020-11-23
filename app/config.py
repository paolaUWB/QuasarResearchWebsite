import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
APP_TMP = os.path.join(basedir, 'tmp')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
