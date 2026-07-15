
from flask import g, request

import extensions
from core.db.exceptions import ColumnNotFoundError, NotFoundError
from core.utils import make_response
from core.app_bp import AppBlueprint
from app.db.exceptions import CategoryNotFoundError

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
        dish = meta_db.dishes.get_from_id(dish_id)

    except NotFoundError as e:
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

    except ColumnNotFoundError as e:
        return make_response(
            3999,
            [e.table, e.name]
        ), 404
    
    except NotFoundError:
        return make_response(
            3002,
            None
        ), 404

    
    

@shop_bp.post("/api/shop/dishes/delete", auth=True, is_admin=True,
              arguments=[{
                "name": "dish_id",
                "type": int,
                "required": True
              }])
def delete_dish():
    dish_id: int = g.args["dish_id"]

    meta_db = get_meta_database()

    try:
        meta_db.dishes.delete(dish_id)
        return make_response(
            0,
            None
        ), 200
    except NotFoundError:
        return make_response(
            3001,
            None
        ), 404
    
@shop_bp.post("/api/shop/dishes/deleteCategory", auth=True, is_admin=True,
              arguments=[
                  {
                      "name": "category_id",
                      "type": int,
                      "required": True
                  }
              ])
def delete_category():
    category_id: int = g.args["category_id"]

    meta_db = get_meta_database()

    # 删除该分类下的所有菜品
    meta_db.dishes.delete_by_category(category_id)

    try:
        meta_db.category.delete(category_id)

        print(category_id)

        name = meta_db.category.get_from_id(category_id)["name"]

        meta_db.category.set_name(category_id, f"{name}_disabled")
        
        return make_response(
            0,
            None
        ), 200
    
    except NotFoundError:
        return make_response(
            3001,
            None
        ), 404
    

@shop_bp.post("/api/shop/dishes/editCategory", auth=True, is_admin=True, 
              arguments=[
                  {
                    "name": "category_id",
                    "type": int,
                    "required": True
                },
                {
                    "name": "category_name",
                    "type": str,
                    "required": True
                }
              ])
def edit_category():
    category_id: int = g.args["category_id"]
    category_name: str = g.args["category_name"]

    meta_db = get_meta_database()

    try:
        meta_db.category.set_name(category_id, category_name)
        return make_response(
            0,
            None
        ), 200
    except NotFoundError:
        return make_response(
            3001,
            None
        ), 404


@shop_bp.post("/api/shop/dishes/new", auth=True, is_admin=True, arguments=[
    {
        "name": "name",
        "type": str,
        "required": True
    },
    {
        "name": "price",
        "type": int, # 单位：分
        "required": True
    },
    {
        "name": "category",
        "type": int,
        "required": True
    },
    {
        "name": "description",
        "type": str,
        "required": False,
        "default": ""
    },
    {
        "name": "image",
        "type": str,
        "required": False,
        "default": ""
    },
    {
        "name": "is_available",
        "type": bool,
        "required": True,
    },
    {
        "name": "choices",
        "type": dict,
        "required": False,
        "default": {}
    }
])
def new_dish():
    name: str = g.args["name"]
    price: int = g.args["price"]
    category: int = g.args["category"]
    description: str = g.args["description"]
    image: str = g.args["image"]
    is_available: bool = g.args["is_available"]
    choices: dict = g.args["choices"]

    meta_db = get_meta_database()

    try:
        dish_id = meta_db.dishes.create(
            name,
            price,
            category,
            description,
            image,
            is_available,
            choices
        )

        return make_response(
            0,
            dish_id
        ), 200 # 创建成功
    
    except CategoryNotFoundError as e:
        return make_response(
            3001,
            e.category_id
        ), 404 # 找不到分类（3001）
    
