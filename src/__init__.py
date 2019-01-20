from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    from src.api import bp as api
    app.register_blueprint(api, url_prefix="/")

    return app