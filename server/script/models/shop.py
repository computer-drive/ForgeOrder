import extensions
from flask import Blueprint, jsonify, request
from libs.utils import make_response
from ..db import get_meta_database
from .exceptions import ArgumentException
from libs.db.exceptions import NotFoundException

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/api/shop/getBusinessState")
def get_business_state():
    return make_response(
        0,
        extensions.is_business
    )

@shop_bp.route("/api/shop/setBusinessState", methods=["POST"])
def set_business_state():
    is_business = request.get_json().get("is_business", False)
    
    extensions.is_business = is_business

    return make_response(
        0,
        None
    )

@shop_bp.route("/api/shop/dishes/getAll")
def get_all_dishes():
    meta_db = get_meta_database()

    dishes, categories = meta_db.dishes.get_all()

    return make_response(
        0,
        {
            "dishes": dishes,
            "categories": categories
        }
    )

@shop_bp.route("/api/shop/dishes/get", methods=["POST"])
def get_dish():
    dish_id = request.get_json().get("id", None)

    if dish_id is None:
        raise ArgumentException(["id"])
    
    meta_db = get_meta_database()

    try:
        dish = meta_db.dishes.get(dish_id)

    except NotFoundException as e:
        return make_response(
            3001,
            None
        )

    return make_response(
        0,
        dict(dish)
    )

    



    