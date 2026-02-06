import os
from flask import Flask, send_from_directory
from app.routes import api


def create_app():
    static_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "static"
    )

    app = Flask(__name__, static_folder=static_folder)
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
