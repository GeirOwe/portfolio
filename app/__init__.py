from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
bootstrap = Bootstrap(app)

#Render deployment

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)