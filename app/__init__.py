from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
bootstrap = Bootstrap(app)

# HEROKU deployment
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku
#
# https://dashboard.heroku.com/apps/garyoinvest
#
# (virtu) $ pip freeze > requirements.txt
# (virtu) geirowe@geirs-imac portfolio % heroku apps:create garyoinvest
# Creating ⬢ garyoinvest... done
# https://garyoinvest.herokuapp.com/ | https://git.heroku.com/garyoinvest.git
# To push the current branch and set the remote as upstream, use
# git push --set-upstream heroku master
# heroku login
# heroku config:set FLASK_APP=main.py
#Procfile: Heroku Procfile.
# web: flask db upgrade; flask translate compile; gunicorn microblog:app
# you first need to make sure that your changes are committed:
#   $ git commit -a -m "heroku deployment changes"
# And then you can run the following to start the deployment:
#   $ git push heroku master
#
#ERROR -> Error R10 (Boot timeout) -> Web process failed to bind to $PORT 
#           within 60 seconds of launch
# Replace "web" with "worker" in your Procfile.
# you need to run heroku ps:scale worker=1 since workers are not scaled 
# automatically (and you should run heroku ps:scale web=0 to remove the 
# web cpu