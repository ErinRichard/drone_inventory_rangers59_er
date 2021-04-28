# functools has a bunch of functions inside of it
from functools import wraps
import secrets

# request verifies when a request comes in
from flask import request, jsonify

from drone_inventory.models import Drone, User

# Similar to login_required
# When we pass our_flask_function into this decorated token_required function, we will have all parameters within the flask_function available to us
def token_required(our_flask_function):
    @wraps(our_flask_function)
    # Create our own decorator
    def decorated(*args, **kwargs):
        # Token none assumes that nobody has a token
        token = None
        
        # place the token in side of x-access-token
        # Relates to bearer in token value in insomnia
        # can view headers using inspect element --> network tab
        if 'x-access-token' in request.headers:
            # split it on a space and give us back the second index
            token = request.headers['x-access-token'].split(' ')[1]
        
        # 401 means 401 response code of unauthorized
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        
        # scoping - the scope only looks at try, and if an error occurs, the interpreter will completely skip over try and head down to except, which is why we have the same variable in both try and except
        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message':'Token is invalid'})

        return our_flask_function(current_user_token, *args, **kwargs)

    return decorated

import decimal
from flask import json


# Price and cost of production will be given to us as decimals, so here we are converting them to strings
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert the decimal value into a string
            return str(obj)
        return super(JSONEncoder, self).default(obj)
