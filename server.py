"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Movies, Ratings



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """Show a list of users with email address and id."""

    users = Users.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<user_id>')
def user_info(user_id):
    """Display user info."""

    return 'hello'


@app.route('/registration_form')
def registration_form():
    """Request email address and password."""

    return render_template('registration_form.html')


@app.route('/new_user', methods=['POST'])
def new_user():
    """Verify unique email and create new user in datebase."""

    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_age = request.form.get('age')
    user_zipcode = request.form.get('zipcode')

    QUERY = Users.query.filter_by(email=user_email).first()

    if QUERY is None:
        user = Users(email=user_email, password=user_password, age=user_age,
                     zipcode=user_zipcode)
        db.session.add(user)
        db.session.commit()

        result = "User created"

    else:
        result = "User exists"

    return f'{result}'


@app.route('/login_form')
def login_form():
    """Request email address and password."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():
    """Validate email and password and update session."""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    QUERY = Users.query.filter_by(email=user_email).first()

    if QUERY is None:
        flash('User does not exist.')
        return redirect('/login_form')

    else:
        QUERY = Users.query.filter_by(email=user_email).first()

        if QUERY.password == user_password:
            session['user_id'] = QUERY.user_id
            flash('Login successful.')
            return redirect('/')

        else:
            flash('Invalid password.')
            return redirect('/login_form')


@app.route('/logout')
def logout():
    """Remove user_id from session."""

    del session['user_id']

    flash('You are now logged out.')
    
    return redirect('/')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
