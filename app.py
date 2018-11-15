#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import table_test
import random as rd

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

PEOPLE_FOLDER = os.path.join('static', 'datateam_photo')


app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
#def about():
#    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'gu.gif')
#    return render_template('pages/placeholder.about.html',user_image = full_filename)
def about():
    full_filenames = [app.config['UPLOAD_FOLDER']+'/' + i for i in os.listdir(app.config['UPLOAD_FOLDER'])]
    rd.shuffle(full_filenames)
    return render_template('pages/placeholder.about.html', user_image = full_filenames)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/sqltest')
def sqltest():
    return render_template('pages/placeholder.menu.html')

@app.route('/table')
def table():
    return render_template('pages/placeholder.menu.html')

@app.route('/lotto')
def lotto():
    return render_template('pages/placeholder.menu.html')

@app.route('/base')
def base():
    return render_template('layouts/base.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
