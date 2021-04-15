import os

# What this does is says 'grab this whole project directory "in-class",
# regardless of which operating system you're on,
# use it the same way

# absolute path - Giving access to the project in ANY OS we find ourselves in
# Allow outside files/folders to have the ability to add to the project from
# the base directory
# Can use relative path also, but absolute eliminates chance of confusion
# and we don't plan to chang ethe nae so we don't really need to worry about it auto-updating
basedir = os.path.abspath(os.path.dirname(__file__))

# create environment variables that Flask will need access to later on
class Config():
    """
    We will set Confi variables for the Flask App here.
    Using Environment variables where available, otherwise
    we will create the confir variable(s) if not already done
    """

    # Setting groundwork for what Flask is going to need 

    # SECRET_KEY allows us to use forms inside of flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...'
    
    # first os.environ.get should work, but If the sqlite file ever appears, we know something is wrong
    # Alchemy is ORM (object relational manager) that allows us to go between Python and Flask
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    # This just prevent excessive errors messages b/c it makes it hard to read in terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Turn off update messages from the database



