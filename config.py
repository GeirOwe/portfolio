import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ALPHA_KEY = os.environ.get('ALPHA_API_KEY')
