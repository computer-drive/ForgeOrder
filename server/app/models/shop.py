from ast import arg

from flask import g, request

import extensions
from core.db.exceptions import NotFoundException
from core.utils import make_response
from core.app_bp import AppBlueprint

from ..db.db import get_meta_database
# from .exceptions import ArgumentException

shop_bp = AppBlueprint("shop", __name__)

@shop_bp.get("/api/shop/getBusinessState" , auth=True)
def get_business_state():
    return make_response(
        0,
        extensions.is_business
    )

@shop_bp.post("/api/shop/setBusinessState",
            auth=True,
            is_admin=True,
            arguments=[
                {
                   "name": "is_business",
                   "type": bool,
                   "required": True
                }
            ])
def set_business_state():
    is_business = g.args["is_business"]
    
    extensions.is_business = is_business

    return make_response(
        0,
        None
    )

@shop_bp.get("/api/shop/dishes/getAll" , auth=True)
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

@shop_bp.post("/api/shop/dishes/get" , auth=True,
              arguments=[
                  {
                      "name": "id",
                      "type": int,
                      "required": True
                  }
              ])
def get_dish():
    dish_id = g.args["id"]


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

    



    