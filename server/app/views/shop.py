import time
from typing import cast



from app.routes.responseGenerator import ResponseInfo
from app.service import SettingsService, ShopService
from app.routes.blueprint import AppBlueprint
from app.routes.field import *
from app.utils import g

shopBlueprint = AppBlueprint("shop", __name__)

# 店铺状态
@shopBlueprint.get("/api/shop/getBusinessState" , requiresAuth=True, 
             responses=[
                 ResponseInfo(0, "OK", bool)
             ])
def getBusinessState():

    service = SettingsService(g.repos)

    isBusiness = service.get("shop.isBusiness")
    
    return g.res.OK(
        isBusiness
    )

@shopBlueprint.post("/api/shop/setBusinessState",
            requiresAuth=True,
            isAdmin=True,
            arguments=[
                BodyField("isBusiness", bool, True)
            ],
            responses=[
                ResponseInfo(0, "OK", None)
            ])
def setBusinessState():
    isBusiness = g.args["isBusiness"]
    
    service = SettingsService(g.repos)

    service.set("shop.isBusiness", isBusiness)

    g.logger.setCategory("Shop")

    g.logger.info("用户 {operator} 更新营业状态：{isBusiness}", {
        "isBusiness": isBusiness,
        "operator": g.userInfo["id"]
    },  "UpdateBusinessState")

    return g.res.OK()



# 菜品
@shopBlueprint.get("/api/shop/dishes/getAll" , requiresAuth=True,
             responses=[
                 ResponseInfo(0, "OK", dict)
             ])
def getAllDishes():

    service = ShopService(g.repos)

    _, data = service.dishes.getAll()

    categories, dishes = cast(tuple, data)

    return g.res.OK(
        {
            "dishes": dishes,
            "categories": categories
        }
    )

@shopBlueprint.post("/api/shop/dishes/get" , requiresAuth=True,
              arguments=[
                  BodyField("id", int, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", dict),
                  ResponseInfo(3001, "DishNotFound", None)
              ])
def getDish():
    dishId = g.args["id"]


    service = ShopService(g.repos)


    status, data = service.dishes.get(dishId)

    if status == service.RESULT.DISH_NOT_FOUND:
        return g.res.DishNotFound()

    

    return g.res.OK(data)

@shopBlueprint.post("/api/shop/dishes/update", requiresAuth=True, isAdmin=True,
              arguments=[
                  BodyField("dishId", int, True),
                  BodyField("changedItems", dict, True),
                  BodyField("changedChoices", list, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "NoChange", None),
                  ResponseInfo(3002, "DishNotFound", None),
                  ResponseInfo(3003, "ChangedItemsNotFound", None), # 更改的信息不存在
                  ResponseInfo(3004, "ChangedItemsValueError", None), # 更改的信息 值非法
                  ResponseInfo(3005, "ChoiceNotFound", None) # 更改的选项不存在
              ])
def updateDish():
    dishId: int = g.args["dishId"]
    changedItems : dict = g.args["changedItems"]
    changedChoices : list = g.args["changedChoices"]

    service = ShopService(g.repos)

    
    if AllOf( # failed
        Not(NotEmpty().bind(changedItems)), # null -> pass
        Not(NotEmpty().bind(changedChoices))  # null -> pass
    ).validate():
        
        return g.res.NoChange()

    g.logger.setCategory("Shop")
    


    status, data = service.dishes.update(dishId, changedItems, changedChoices)

    match status:
        case service.RESULT.SUCCESS:

            g.logger.info("用户 {operator} 更新菜品 {id} 的信息", {
                "id": dishId,
                "changedItems": changedItems,
                "changedChoices": changedChoices
            }, "UpdateDish")
            
            return g.res.OK()

        case service.RESULT.CHANGED_ITEMS_NOT_FOUND:
            return g.res.ChangedItemsNotFound({
                "id": dishId,
                "key": data
            })

        case service.RESULT.DISH_NOT_FOUND:
            return g.res.DishNotFound({
                "id": dishId
            })

        case service.RESULT.VALUE_ERROR:
            return g.res.ChangedItemsValueError({
                "id": dishId,
            })

        case service.RESULT.CHOICE_NOT_FOUND:
            return g.res.ChoiceNotFound({
                "id": dishId,
                "name": data
            })




@shopBlueprint.post("/api/shop/dishes/delete", requiresAuth=True, isAdmin=True,
               arguments=[
                   BodyField("dishId", int, True)
               ],
               responses=[
                   ResponseInfo(0, "OK", None),
                   ResponseInfo(3001, "DishNotFound", None)
               ])
def deleteDish():
    dishId: int = g.args["dishId"]

    service = ShopService(g.repos)

    g.logger.setCategory("Shop")
    
    
    status, data = service.dishes.delete(dishId)

    if status == service.RESULT.DISH_NOT_FOUND:
        return g.res.DishNotFound()

    return g.res.OK()
    
@shopBlueprint.post("/api/shop/dishes/new", requiresAuth=True, isAdmin=True, arguments=[
    BodyField("name", str, True, None, NotEmpty()),
    BodyField("price", int, True, None, Interval(Open(0), None)),
    BodyField("category", int, True),
    BodyField("description", str, False, ""),
    BodyField("image", str, False, ""),
    BodyField("isAvailable", bool, True),
    BodyField("choices", dict, False, {})
],
responses=[
    ResponseInfo(0, "OK", None),
    ResponseInfo(3001, "CategoryNotFound", None)
]
)
def newDish():
    name: str = g.args["name"]
    price: int = g.args["price"]
    category: int = g.args["category"]
    description: str = g.args["description"]
    image: str = g.args["image"]
    isAvailable: bool = g.args["isAvailable"]
    choices: dict = g.args["choices"]

    service = ShopService(g.repos)

    g.logger.setCategory("Shop")

    status, data = service.dishes.create(name, price, category, description, isAvailable, choices)

    if status == service.RESULT.CATEGORY_NOT_FOUND:
        return g.res.CategoryNotFound()

    return g.res.OK()
    
    

# 分类
@shopBlueprint.post("/api/shop/category/delete", requiresAuth=True, isAdmin=True,
              arguments=[
                  BodyField("categoryId", int, True)
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNotFound", None)
              ])
def deleteCategory():
    categoryId: int = g.args["categoryId"]


    g.logger.setCategory("Shop")

    service = ShopService(g.repos)

    service.dishes.deleteByCategory(categoryId)

    result, data = service.dishesCategory.delete(categoryId)

    if result == service.RESULT.CATEGORY_NOT_FOUND:
        return g.res.CategoryNotFound()
    
    return g.res.OK()

@shopBlueprint.get("/api/shop/category/getAll" , requiresAuth=True, 
             responses=[
                 ResponseInfo(0, "OK", None)
             ])
def getAllCategories():

    service = ShopService(g.repos)

    return g.res.OK(    
        service.dishesCategory.getAll().data
    )


@shopBlueprint.post("/api/shop/category/update", requiresAuth=True, isAdmin=True, 
              arguments=[
                  BodyField("categoryId", int, True),
                  BodyField("categoryName", str, True, None, NotEmpty())
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNotFound", None)
              ])
def editCategory():
    categoryId: int = g.args["categoryId"]
    categoryName: str = g.args["categoryName"]

    service = ShopService(g.repos)

    g.logger.setCategory("Shop")

    status, data = service.dishesCategory.update(categoryId, categoryName)

    if status == service.RESULT.CATEGORY_NOT_FOUND:
        return g.res.CategoryNotFound()
        
    return g.res.OK()

@shopBlueprint.post("/api/shop/category/new", requiresAuth=True, isAdmin=True,
              arguments=[
                  BodyField("name", str, True, None, NotEmpty())
              ],
              responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "CategoryNameExist", None)
              ])
def newCategory():
    
    name: str = g.args["name"]


    g.logger.setCategory("Shop")


    service = ShopService(g.repos)
    status, data = service.dishesCategory.create(name)

    if status == service.RESULT.CATEGORY_ALREADY_EXIST:
        return g.res.CategoryNameExist()
    
    return g.res.OK()
     
# 桌台
@shopBlueprint.get("/api/shop/tables/getAll", requiresAuth=True, responses=[
                  ResponseInfo(0, "OK", None)
              ])
def getAllTables():

    service = ShopService(g.repos)



    status, data = service.tables.getAll()

    return g.res.OK(
        data
    )

@shopBlueprint.post("/api/shop/tables/new", requiresAuth=True, isAdmin=True,
             arguments=[
                  BodyField("name", str, True, None, NotEmpty())
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNameExist", None)
             ])
def newTable():
    name: str = g.args["name"]

    service = ShopService(g.repos)

    g.logger.setCategory("Shop")

    status, data = service.tables.create(name)

    if status == service.RESULT.TABLE_ALREADY_EXIST:
        return g.res.TableNameExist()

    operator = g.userInfo["id"]

    g.logger.info("用户 {operator} 创建桌台 {name}", {
            "id": data,
            "name": name,
            "operator": operator
        }, "NewTable")
        
    return g.res.OK()

@shopBlueprint.post("/api/shop/tables/update", requiresAuth=True, isAdmin=True,
             arguments=[
                  BodyField("id", int, True),
                  BodyField("name", str, True, None, NotEmpty())
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNotFound", None),
                  ResponseInfo(3002, "TableNameExist", None)
             ])
def updateTable():
    tableId: int = g.args["id"]
    newName: str = g.args["name"]

    service = ShopService(g.repos)

    g.logger.setCategory("Shop")


    status, data = service.tables.update(tableId, newName)

    if status == service.RESULT.TABLE_NOT_FOUND:
        return g.res.TableNotFound()
    elif status == service.RESULT.TABLE_ALREADY_EXIST:
        return g.res.TableNameExist()
    else:
        g.logger.info("用户 {operator} 更新桌台 {id} 的名称为 {name}", {
                "id": tableId,
                "name": newName,
                "operator": g.userInfo["id"]
            }, "UpdateTable")
        
        return g.res.OK()

@shopBlueprint.post("/api/shop/tables/delete", requiresAuth=True, isAdmin=True,
             arguments=[
                  BodyField("id", int, True)
             ],
             responses=[
                  ResponseInfo(0, "OK", None),
                  ResponseInfo(3001, "TableNotFound", None)
             ])
def deleteTable():
    tableId = g.args["id"]

    service = ShopService(g.repos)

    result, data = service.tables.delete(tableId)

    if result == service.RESULT.TABLE_NOT_FOUND:
        return g.res.TableNotFound()

    return g.res.OK()

@shopBlueprint.post("/api/shop/tables/get", requiresAuth=True, arguments=[
    BodyField("id", int, True)
], responses=[
    ResponseInfo(0, "OK", None),
    ResponseInfo(3001, "TableNotFound", None)
])
def getTable():
    tableId = g.args["id"]

    service = ShopService(g.repos)

    result, data = service.tables.get(tableId)

    if result == service.RESULT.TABLE_NOT_FOUND:
        return g.res.TableNotFound(data)

    return g.res.OK(data)





