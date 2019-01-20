from flask import Blueprint, request as r, jsonify
import src.analyser as nn
from googlemaps import Client

maps = Client("AIzaSyClSNKv2amm5QqdHjD4wniQO9sLHXjeslg")
print('loading analyser')
nn.init()
print('done')

bp = Blueprint("api", __name__)

@bp.route("/summarise", method=["GET"])
def place():
    place_id = r.args.get('id')
    return jsonify(maps.place(place_id, fields=["review"]))



@bp.route("/summarise", methods=["POST"])
def summerize():
    text = r.get_json()["text"]
    result = nn.analyse(text)
    return jsonify(result)

