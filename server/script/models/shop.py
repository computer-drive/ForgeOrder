import extensions
from flask import Blueprint, jsonify, request
from libs.utils import make_response

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/api/shop/getBusinessState")
def get_business_state():
    return jsonify(make_response(
        0,
        extensions.is_business
    ))

@shop_bp.route("/api/shop/setBusinessState", methods=["POST"])
def set_business_state():
    is_business = request.get_json().get("is_business", False)
    
    extensions.is_business = is_business

    return jsonify(make_response(
        0,
        None
    ))
