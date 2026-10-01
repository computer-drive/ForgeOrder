from app.routes.responseGenerator import ResponseInfo as _Res
from app.utils import g
from app.routes.blueprint import AppBlueprint
from app.routes.field import BodyField as _Field
from app.routes.field import NotEmpty, Choices, Interval, AllOf, DictOf, ForEach
from app.service import OrderService

ordersBlueprint = AppBlueprint("orders", __name__)

@ordersBlueprint.post("/api/order/new", requiresAuth=True, isAdmin=True,
    arguments=[
        _Field("orderType", int, True, None, Choices(0, 1)),
        _Field("partySize", int, True, None, Interval(0, None)),
        _Field("tableId", int, True, None),
        _Field("dishes", list, True, None, 
            AllOf(NotEmpty(), ForEach(DictOf().\
                Field("id", int, True).\
                Field("count", int, True, Interval(1, None)).\
                Field("choices", dict, True)
        ))),
        _Field("note", str, True, None)
    ],
    responses=[
        _Res(0, "OK", None),
        _Res(3011, "TableNotFound", None),
        _Res(3012, "TableNotAvailable", None),
        _Res(3021, "DishNotFound", None),
        _Res(3022, "DishNotAvailable", None),
        _Res(3023, "DishChoiceNotFound", None),
        _Res(3024, "DishChoiceOptionNotFound", None),
        _Res(3031, "OrderAlreadyExist", None),
        _Res(3999, "UnknownError", None)

    ]
)
def newOrder():
    orderType: int = g.args["orderType"]
    partySize: int = g.args["partySize"]
    tableId: int = g.args["tableId"]
    dishes: list[dict] = g.args["dishes"]
    note: str = g.args["note"]

    creator = g.userInfo["id"]

    service = OrderService(g.repos)

    status, data = service.new(orderType, tableId, partySize, dishes, note, creator) #type: ignore

    match status:
        case service.RESULT.SUCCESS:
            return g.res.OK(data)
        case service.RESULT.TABLE_NOT_FOUND:
            return g.res.TableNotFound(tableId)
        case service.RESULT.TABLE_NOT_AVAILABLE:
            return g.res.TableNotAvailable(tableId)
        case service.RESULT.DISH_NOT_FOUND:
            return g.res.DishNotFound(data)
        case service.RESULT.DISH_NOT_AVAILABLE:
            return g.res.DishNotAvailable(data)
        case service.RESULT.DISH_CHOICE_NOT_FOUND:
            return g.res.DishChoiceNotFound(data)
        case service.RESULT.DISH_CHOICE_OPTION_NOT_FOUND:
            return g.res.DishChoiceOptionNotFound(data)
        case service.RESULT.ORDER_ALREADY_EXIST:
            return g.res.OrderAlreadyExist()

        case _:
            g.logger.setCategory("Order")

            g.logger.warning(str(status), "UnknownResult")

            return g.res.UnknownError({
                "errorCode": str(status),
                "errorInfo": str(data)
            })

@ordersBlueprint.post("/api/order/getToday", requiresAuth=True,
    arguments=[
    _Field("offset", int, False, 0, AllOf(Interval(0, None))),
    _Field("limit", int, False, 10, AllOf(Interval(0, None)))
],
    responses=[
    _Res(0, "OK", None)
])
def getTodayOrders():
    offset = g.args["offset"]
    limit = g.args["limit"]

    service = OrderService(g.repos)

    status, data = service.getToday(offset, limit)

    return g.res.OK(data)

@ordersBlueprint.post("/api/order/get", requiresAuth=True,
    arguments=[
        _Field("id", str, True, None),
        _Field("queries", list, True, None, ForEach(Choices("tableName", "subOrdersCount", "dishesCount", "basicInfo")))
    ], responses=[
        _Res(0, "OK", None),
        _Res(3001, "PartialError", None),
        _Res(3999, "UnknownError", None),
        _Res(3002, "OrderNotFound", None)
])
def getOrder():
    orderId = g.args["id"]
    queries = g.args["queries"]

    service = OrderService(g.repos)

    status, data = service.get(orderId, queries)

    if status == service.RESULT.SUCCESS:
        return g.res.OK(data)
    elif status == service.RESULT.HAS_PARTIAL_ERROR:
        return g.res.PartialError(data)
    elif status == service.RESULT.ORDER_NOT_FOUND:
        return g.res.OrderNotFound()
    else:
        g.logger.setCategory("Orders")

        # g.logger.warning(str(status), "UnknownError")

        return g.res.UnknownError()