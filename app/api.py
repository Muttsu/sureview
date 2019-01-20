from flask import Blueprint, request as r, jsonify
import app.analyser as nn

bp = Blueprint("api", __name__)

@bp.route("/summerize", method=["GET"])
def place():
    place_id = r.args.get('id')
    return place_id



@bp.route("/summerize", methods=["POST"])
def summerize():
    text = r.get_json()["text"]
    result = nn.analyse(text)
    return jsonify(result)

