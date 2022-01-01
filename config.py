import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))