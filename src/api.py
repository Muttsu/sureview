from flask import Blueprint, request as r, jsonify
import src.analyser as nn
from googlemaps import Client

maps = Client("AIzaSyClSNKv2amm5QqdHjD4wniQO9sLHXjeslg")
print('loading analyser')
nn.init()
print('done')

bp = Blueprint("api", __name__)

@bp.route("/summarise", methods=["GET"])
def place():
    place_id = r.args.get('id')
    result = maps.place(place_id, fields=["review"])
    reviews = [r['text'] for r in result['result']['reviews']]
    return jsonify(nn.analyse("\n".join(reviews)))




@bp.route("/summarise", methods=["POST"])
def summerize():
    text = r.get_json()["text"]
    result = nn.analyse(text)
    return jsonify(result)

