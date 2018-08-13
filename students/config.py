import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '9=iensbkbpl#*%s)q(0ts=)o4co%(3_l_&85v+px=asu$icm$j'

    # The DB credential has been hardcoded only for Project demo. Never write credentials to file.
    # Replace user and password with your mysql password respedtively.
    # This should work with other SQL database too. Try by changing mysql:// to your DB.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://user:password@localhost/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
