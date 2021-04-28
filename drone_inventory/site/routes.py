from flask import Blueprint, render_template
from flask_login import login_required


# Create a variable called 'site' - which is the name we gave to our blueprint
# Arguments for Blueprint are: (blueprint_name, import_name, template_folder)
# Read documentation for blueprints: https://flask.palletsprojects.com/en/1.1.x/blueprints/
site = Blueprint('site', __name__, template_folder='site_templates')

"""
Blueprint Configuration
The first argument, called 'site', is the Blueprint's name,
which is used for Flask's routing system.

The second argument, __name__, is the Blueprint's import name, 
which Flask uses to locate the Blueprint resources.

The last argument, 'template_folder', is the Blueprint's HTML template folder,
which tells the Blueprint which HTML files to use for specific routes.
"""

# This is a function that takes one parameter '/'
# Look at Flask documentation for additional explanation regarding '@' below
# We're saying that this is going to be our main page
# a route inside of flask is the url with a forward slash and something after it
# The @ is routing us to the main page
# Specify the route variable
@site.route('/')
def home():
    return render_template('index.html') # Add render_template to import stmt above

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



