
from flask import g, request

import extensions
from core.db.exceptions import ColumnNotFoundException, NotFoundException
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

@shop_bp.get("/api/shop/dishes/getAllCategories" , auth=True)
def get_all_categories():
    meta_db = get_meta_database()

    categories = meta_db.category.get_all()
    categories = [dict(category) for category in categories]

    return make_response(
        0,
        categories
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
        ), 404


    return make_response(
        0,
        dict(dish)
    )

@shop_bp.post("/api/shop/dishes/update", auth=True, is_admin=True,
              arguments=[{
                "name": "dish_id",
                "type": int,
                "required": True
              },
              {
                  "name": "changed_items",
                  "type": dict,
                  "required": True
              },
              {
                  "name": "changed_choices",
                  "type": list,
                  "required": True
              }])
def update_dish():
    dish_id: int = g.args["dish_id"]
    changed_items : dict = g.args["changed_items"]
    changed_choices : list = g.args["changed_choices"]

    meta_db = get_meta_database()

    if len(changed_items.values()) == 0 and len(changed_choices) == 0:
        return make_response(
            3001,
            None
        ), 400

    extensions.logger.debug([dish_id, changed_items, changed_choices], "UPDATE_DISH_REQUEST", "DebugMsg")

    try:
        meta_db.dishes.update(dish_id, changed_items, changed_choices)
        
        return make_response(
            0,
            None
        ), 200

    except ColumnNotFoundException:
        return make_response(
            3002,
            None
        ), 404


    

    



    