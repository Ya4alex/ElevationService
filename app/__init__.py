from flask import Flask
from flask_cors import CORS
from config import config


def create_app():
    app = Flask(
        __name__,
        static_url_path=config.STATIC_URL,
        static_folder=config.STATIC_DIR,
    )
    CORS(app)
    app.config.from_object('config.config')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
