from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World"

    from src.api import bp as api
    app.register_blueprint(api, url_prefix="/")

    return app