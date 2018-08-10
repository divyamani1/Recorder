import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '9=iensbkbpl#*%s)q(0ts=)o4co%(3_l_&85v+px=asu$icm$j'

    # The DB credential has been hardcoded only for Project demo. Never write credentials to file.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://user:password@localhost/students'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
