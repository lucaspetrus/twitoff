from flask import Flask

app = Flask(__name__)


def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)

    # things to do to make the app
    @app.route('/')
    def root():
        return 'Hello, TwitOff'

    return app
