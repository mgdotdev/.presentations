from flask import Blueprint, jsonify

bp = Blueprint("v1", __name__)


@bp.get("/")
def _():
    return jsonify({
        "response": "this is the root of the flask API"
    })
