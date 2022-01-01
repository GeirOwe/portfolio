from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
bootstrap = Bootstrap(app)

# (virtu) $ pip freeze > requirements.txt
# (virtu) geirowe@geirs-imac portfolio % heroku apps:create garyoinvest
# Creating ⬢ garyoinvest... done
# https://garyoinvest.herokuapp.com/ | https://git.heroku.com/garyoinvest.git
# To push the current branch and set the remote as upstream, use
# git push --set-upstream heroku master