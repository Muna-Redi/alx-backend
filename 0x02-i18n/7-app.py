#!/usr/bin/env python3
"""Flask app """


from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone
import pytz.exceptions


class Config(object):
    ''' Language  configuration '''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# configure the flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """ This returna user dictionary or None if ID not foundn"""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """ decorator for pre-request """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    ''' best-match language via user locale '''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Pick  and return appropriate timezone
    """
    # timezone parameter in URL parameters
    time_zone = request.args.get('timezone', None)
    if time_zone:
        try:
            return timezone(time_zone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    # time zone from user settings
    if g.user:
        try:
            time_zone = g.user.get('timezone')
            return timezone(time_zone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    # Default
    default_time_zone = app.config['BABEL_DEFAULT_TIMEZONE']
    return default_tme_zone


@app.route('/')
def index():
    ''' Babel usage route'''
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
