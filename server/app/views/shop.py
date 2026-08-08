import time

from flask import g, request

from app.app_settings.manager import SettingsManager
from app.routes.res_generator import ResponseInfo
from core.db.exceptions import ColumnNotFoundError, NotFoundError
from core.utils import make_response
from app.routes.app_bp import AppBlueprint
from app.db.main_db.exceptions import CategoryNotFoundError
from ..db.get_db import get_database_flask
from app.routes.field import *

shop_bp = AppBlueprint("shop", __name__)

# 店铺状态
@shop_bp.get("/api/shop/getBusinessState" , auth=True, 
             responses=[
                 ResponseInfo(0, "OK", bool)
             ])
def get_business_state():
    db = get_database_flask()
    sm = SettingsManager(db)

    is_business = sm.get("shop.isBusiness")
    
    return g.res.OK(
        0,
        is_business
    )

@shop_bp.post("/api/shop/setBusinessState",
            auth=True,
            is_admin=True,
            arguments=[
                RequestField("is_business", bool, True)
            ],
            responses=[
                ResponseInfo(0, "OK", None)
            ])
def set_business_state():
    is_business = g.args["is_business"]
    
    db = get_database_flask()
    sm = SettingsManager(db)

    sm.set("shop.isBusiness", is_business)

    g.logger.set_category("SHOP")

    g.logger.info({
        "is_business": is_business,
        "operator": g.user_info["user"]["id"]
    },  "UpdateBusinessState")

    return g.res.OK()



# 菜品
@shop_bp.get("/api/shop/dishes/getAll" , auth=True,
             responses=[
                 ResponseInfo(0, "OK", dict)
             ])
def get_all_dishes():
    db = get_database_flask()

    dishes, categories = db.dishes.get_all()

    return g.res.OK(
        {
            "dishes": dishes,
            "categories": categories
        }
    )

@shop_bp.post("/api/shop/dishes/get" , auth=True,
              arguments=[
                  RequestField("id", int, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", dict),
                  ResponseInfo(3001, "DishNotFound", None)
              ])
def get_dish():
    dish_id = g.args["id"]


    db = get_database_flask()

    try:
        dish = db.dishes.get_from_id(dish_id)

    except NotFoundError as e:
        return g.res.DishNotFound()


    return g.res.OK(dict(dish))

@shop_bp.post("/api/shop/dishes/update", auth=True, is_admin=True,
              arguments=[
                  RequestField("dish_id", int, True),
                  RequestField("changed_items", dict, True),
                  RequestField("changed_choices", list, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "NoChange", None),
                  ResponseInfo(3002, "DishNotFound", None)
              ])
def update_dish():
    dish_id: int = g.args["dish_id"]
    changed_items : dict = g.args["changed_items"]
    changed_choices : list = g.args["changed_choices"]

    db = get_database_flask()

    
    if AllOf( # failed
        Not(NotEmpty().bind(changed_items)), # null -> pass
        Not(NotEmpty().bind(changed_choices))  # null -> pass
    ).validate():
        
        return g.res.NoChange()

    g.logger.set_category("SHOP")
    


    try:
        db.dishes.update(dish_id, changed_items, changed_choices)

        g.logger.info({
            "id": dish_id,
            "changed_items": changed_items,
            "changed_choices": changed_choices
        }, "UpdateDish")
        
        return g.res.OK()

    except NotFoundError:
        return g.res.DishNotFound()

@shop_bp.post("/api/shop/dishes/delete", auth=True, is_admin=True,
               arguments=[
                   RequestField("dish_id", int, True)
               ],
               responses=[
                   ResponseInfo(0, "OK", None),
                   ResponseInfo(3001, "DishNotFound", None)
               ])
def delete_dish():
    dish_id: int = g.args["dish_id"]

    db = get_database_flask()

    g.logger.set_category("SHOP")
    
    
    try:
        db.dishes.delete(dish_id)

        g.logger.info({
                "id": dish_id
            }, "DeleteDish")

        
        return g.res.OK()
    except NotFoundError:
        return g.res.DishNotFound()
    
@shop_bp.post("/api/shop/dishes/new", auth=True, is_admin=True, arguments=[
    RequestField("name", str, True, None, NotEmpty()),
    RequestField("price", int, True, None, Interval(Open(0), None)),
    RequestField("category", int, True),
    RequestField("description", str, False, ""),
    RequestField("image", str, False, ""),
    RequestField("is_available", bool, True),
    RequestField("choices", dict, False, {})
],
responses=[
    ResponseInfo(0, "OK", None),
    ResponseInfo(3001, "CategoryNotFound", None)
]
)
def new_dish():
    name: str = g.args["name"]
    price: int = g.args["price"]
    category: int = g.args["category"]
    description: str = g.args["description"]
    image: str = g.args["image"]
    is_available: bool = g.args["is_available"]
    choices: dict = g.args["choices"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        dish_id = db.dishes.create(
            name,
            price,
            category,
            description,
            image,
            is_available,
            choices
        )

        g.logger.info({
            "id": dish_id,
            "name": name,
            "price": price,
            "category": category,
            "description": description,
            "image": image,
            "is_available": is_available,
            "choices": choices
        }, "NewDish")

        return g.res.OK()
    
    except CategoryNotFoundError as e:
        return g.res.CategoryNotFound()
    

# 分类
@shop_bp.post("/api/shop/category/delete", auth=True, is_admin=True,
              arguments=[
                  RequestField("category_id", int, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNotFound", None)
              ])
def delete_category():
    category_id: int = g.args["category_id"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        name = db.category.get_from_id(category_id)["name"]

        # 先验证分类存在，再删除该分类下的所有菜品
        db.dishes.delete_by_category(category_id)

        db.category.update(category_id, f"{name}_disabled_{time.time()}")

        db.category.delete(category_id)

        g.logger.info({
                "id": category_id
            }, "DeleteCategory")
        
        return g.res.OK()
    
    except NotFoundError as e :

        return g.res.CategoryNotFound()

@shop_bp.get("/api/shop/category/getAll" , auth=True)
def get_all_categories():
    db = get_database_flask()

    categories = db.category.get_all()
    categories = [dict(category) for category in categories]

    return make_response(
        0,
        categories
    )


@shop_bp.post("/api/shop/category/update", auth=True, is_admin=True, 
              arguments=[
                  RequestField("category_id", int, True),
                  RequestField("category_name", str, True, None, NotEmpty())
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNotFound", None)
              ])
def edit_category():


    category_id: int = g.args["category_id"]
    category_name: str = g.args["category_name"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        db.category.update(category_id, category_name)

        g.logger.info({
                "id": category_id,
                "name": category_name
            }, "UpdateCategory")

        return g.res.OK()
    
    except NotFoundError:
        return g.res.CategoryNotFound()

@shop_bp.post("/api/shop/category/new", auth=True, is_admin=True,
              arguments=[
                  RequestField("name", str, True, None, NotEmpty())
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNameExist", None)
              ])
def new_category():
    
    name: str = g.args["name"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        category_id = db.category.new(name)

        g.logger.info({
                "id": category_id,
                "name": name
            }, "NewCategory")
        
        return g.res.OK()
    except ValueError:
        return g.res.CategoryNameExist()
     

@shop_bp.get("/api/shop/tables/getAll", auth=True, responses=[
                  ResponseInfo(0, "OK", None)
              ])
def get_all_tables():
    db = get_database_flask()

    tables = db.tables.get_all()

    return g.res.OK(
        tables
    )

@shop_bp.post("/api/shop/tables/new", auth=True, is_admin=True,
             arguments=[
                  RequestField("name", str, True, None, NotEmpty())
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNameExist", None)
             ])
def new_table():
    name: str = g.args["name"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        table_id = db.tables.new(name, True)
    except ValueError:

        return g.res.TableNameExist()
    else:
        g.logger.info({
                "id": table_id,
                "name": name
            }, "NewTable")
        
        return g.res.OK()

@shop_bp.post("/api/shop/tables/update", auth=True, is_admin=True,
             arguments=[
                  RequestField("id", int, True),
                  RequestField("name", str, True, None, NotEmpty())
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNotFound", None),
                  ResponseInfo(3002, "TableNameExist", None)
             ])
def update_table():
    table_id: int = g.args["id"]
    new_name: str = g.args["name"]

    db = get_database_flask()

    g.logger.set_category("SHOP")

    try:
        db.tables.update(table_id, new_name, True)
    except NotFoundError:
        return g.res.TableNotFound()

    except ValueError:
        return g.res.TableNameExist()
    
    else:
        g.logger.info({
                "id": table_id,
                "name": new_name
            }, "UpdateTable")
        
        return g.res.OK()

@shop_bp.post("/api/shop/tables/delete", auth=True, is_admin=True,
             arguments=[
                  RequestField("id", int, True)
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNotFound", None)
             ])
def delete_table():
    table_id: int = g.args["id"]


    db = get_database_flask()
    g.logger.set_category("SHOP")

    try:
        db.tables.soft_delete(table_id)

    except NotFoundError:
        return g.res.TableNotFound()
    else:
        g.logger.info({
                "id": table_id
            }, "DeleteTable")
        
        return g.res.OK()




