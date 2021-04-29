from flask_sqlalchemy import SQLAlchemy

# import uuid library from Python (universal unique identifier)
import uuid

from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Provided by Python)
import secrets

# Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

# Step 2 is passing this database reference to init.py
db = SQLAlchemy()
login_manager = LoginManager()

ma = Marshmallow()

# Return/get the user that's logged in based on the user id
# The query.get syntax is the same as SELECT id from USER table WHERE ID == 'whatever'
# The only reason we can access user id is because we get it from user_loader
# user_loader gets it from the @ decorator
# user_loader is a callback method --> passing user_id into database
# gives us access to the user id based on the session cookie from the browser
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Step 1
# This class will create the database table for us
class User(db.Model, UserMixin):
    # The id db.String will eventually become a VARCHAR
    # Allow String here to work better with Python (than how we used SERIAL when first learning Postgres in week 4)
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    
    # nullable = False means that it cannot be empty
    email = db.Column(db.String(150), nullable = False)
    
    # No limit on the password length. We will encrypt this
    # Password is required
    password = db.Column(db.String, nullable = False, default = '')
    
    # Unique = True means that nothing can be duplicated within a token
    token = db.Column(db.String, default ='', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # Lazy means relationship will only be available when needed and no other time otherwise
    drone = db.relationship('Drone',backref = 'owner', lazy = True)

    def __init__(self, email,first_name = '', last_name='', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    # Used for authentication for users to view only their drones
    # Not a token like I used to have for BofA 
    # It's stored in the user info
    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        # password gets changed into a hashable value
        # the hashable value gets passed to self.pw_hash
        self.pw_hash = generate_password_hash(password)
        # set_password has a returnable value
        # self.pw_hash is what's returned to self.password
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'


class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    # Precision means we will have 10 available spaces for numeric value with 2 decimal places at the end of it
    price = db.Column(db.Numeric(precision=10, scale = 2))
    cam_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    # Cost of production
    cost_of_prod = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(150))
    # Specify Foriegn Key relationship in the () after db.ForeignKey
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    # id goes at the end of the list
    def __init__(self, name, description, price, cam_quality, flight_time, max_speed, dimensions, weight, cost_of_prod, series, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.cam_quality = cam_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f'The following Drone has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()


# Creation of API Schema via the marshmallow package
class DroneSchema(ma.Schema):
    class Meta:
        # Don't want to expose the token for the user, so not included here
        # This is what we should see as the end result of the json in Insomnia
        # Asking the Schema to create the look and feel of our results
        fields = ['id', 'name', 'description', 'price', 'cam_quality,' 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']

drone_schema = DroneSchema()
# many = True means it should display the results in a list if many drones are available/entered
drones_schema = DroneSchema(many = True)