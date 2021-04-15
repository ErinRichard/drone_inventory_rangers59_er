# This init file tells us that name of our project is drone_inventory, and you'll find it inside of drone_inventory

# Import the Flask class
from flask import Flask

# Import the Config class that we created in the config.py file
from config import Config

# Import the 'site' blueprint that we created in routes.py
# Need .site (not just site because drone_inventory is the parent. The . in front takes us through the path) 
from .site.routes import site

from .authentication.routes import auth
from .api.routes import api

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

# Cross Origin Resource Sharing - turned off by default because it helps prevent malicious people sending things from one domain to another. We want to turn it on for development
from flask_cors import CORS

from .helpers import JSONEncoder


# Create an instance of the class
app = Flask(__name__)

app.config.from_object(Config)

# Register the application/blueprint
# Need to import the site blueprint into this file
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

root_db.init_app(app)
migrate = Migrate(app, root_db)

# Need to import login_manager
login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # specify what page to load for NON-AUTHED users

ma.init_app(app)

# The CORS(app) statement turns on CORS to allow cross-domain sharing because it's turned off by default. We want it on for our purposes during development
CORS(app)

app.json_encoder = JSONEncoder

from drone_inventory import models