from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db, check_password_hash

# Imports for flask login
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# Two methods GET -> gets the form and POST -> allows the form to post
@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    # specify where data is going to come from
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # Print just to confirm it worked
            print(email, password)

            # Password is a keyword, so we have specify which one
            user = User(email, password = password)

            # Equivalent of an insert statement
            # Here we are inserting a user
            # From the models file
            db.session.add(user)

            # To actually place the info inside of the database
            # From the models file
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        # verifying that the form is posting - see form.html (if the form has a method of POST, and also the email is an actual email, and the password is present, then the form is valid)
        if request.method == 'POST' and form.validate_on_submit():
            # if true, get the email from the form
            email = form.email.data
            password = form.password.data
            # Print just to check to make sure it's working
            print(email,password)

            # Similar to a WHERE clause in SQL
            # Looking for User email that's set equal to what comes from the form
            # Need to add .first method to secify that we are looking for the user email that has been passed using the form (won't work properly without .first() - just shows SQL code - kind of grabbing the row from the SQL table)
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: via email/password', 'auth-success')
                return redirect(url_for('site.home'))

            # If login unsuccessful, show this message
            # 'auth-failed' is called a category (can name it anything you want, and will reference it on appropriate html page)
            # example {% if cat == 'user-created' %}
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form!')

    return render_template('signin.html', form=form)


# Set up logout route
# In order for this to work, we need to make some changes to base.html
@auth.route('/logout')
# Need to import login_required
@login_required
def logout():
    # Need to import logout_user
    logout_user()
    return redirect(url_for('site.home'))