from enum import Enum, auto
from typing import TypedDict, Literal, cast
import datetime
import uuid

from app.service.shop import ShopService
from .base import Service, Result
from ..db.repository.orders import _OrdersRow, _SubOrdersRow, _OrderItemsRow
from core.utils.common import uuidToShortCode

class ResultCode(Enum):
    INVALID_ORDER_TYPE = auto() # 订单类型不正确

    INVALID_PARTY_SIZE = auto() # 订单人数不正确

    TABLE_NOT_FOUND = auto() # 桌台不存在
    TABLE_NOT_AVAILABLE = auto() # 桌台不可用

    CREATOR_NOT_FOUND = auto()

    DISH_NOT_FOUND = auto()
    DISH_COUNT_NOT_AVAILABLE = auto()
    DISH_NOT_AVAILABLE = auto()
    DISH_CHOICE_NOT_FOUND = auto()
    DISH_CHOICE_OPTION_NOT_FOUND = auto()

    ORDER_ALREADY_EXIST = auto()

    # 成功
    SUCCESS = auto()

    ORDER_NOT_FOUND = auto() # 找不到订单
    HAS_PARTIAL_ERROR = auto()

class DishesDict(TypedDict):
    id: int
    count: int
    choices: dict

# 找不到菜品异常
class OrderNotFoundError(Exception): ... 

class OrderService(Service):
    RESULT = ResultCode

    def new(self,
            orderType: int,
            tableId: int,
            partySize: int,
            dishes: list[DishesDict],
            note: str,
            creatorId: int):

        # 判断订单类型
        if orderType not in (0, 1):
            return Result(self.RESULT.INVALID_ORDER_TYPE)

        # 判断partySize
        if partySize <= 0:
            return Result(self.RESULT.INVALID_PARTY_SIZE)

        # 查询数据库获取桌台信息
        if orderType == 0:
            table = self.repos.tables.get(id=tableId)

            if table is None:
                return Result(self.RESULT.TABLE_NOT_FOUND)
            elif not table["isAvailable"]:
                return Result(self.RESULT.TABLE_NOT_AVAILABLE)


        # 查询数据库判断用户是否存在
        creator = self.repos.users.get(id=creatorId)

        if creator is None:
            return Result(self.RESULT.CREATOR_NOT_FOUND, creatorId)

        # 查询数据库获取订单信息
        dishesInfo = []
        totalPrice = 0

        for dish in dishes:
            # 判断 count 是否有效
            if dish["count"] <= 0:
                return Result(self.RESULT.DISH_COUNT_NOT_AVAILABLE, dish["id"])
            
            # 获取菜品信息
            dishInfo = self.repos.dishes.get(id=dish["id"], isDeleted=False) #type: ignore

            if dishInfo is None:
                #找不到菜品
                return Result(self.RESULT.DISH_NOT_FOUND, dish["id"])

            if dishInfo["isAvailable"] is False:
                # 菜品不可用
                return Result(self.RESULT.DISH_NOT_AVAILABLE, dish["id"])

            # 获取菜品选项信息
            dishChoicesInfo = self.repos.dishChoices.getAll(dishId=dish["id"])
            choicesNameMap = {c["name"]: c for c in dishChoicesInfo} # 构建索引以快速查找

            for choice, option in dish["choices"].items():
                # 判断菜品的选项是否存在
                if choice not in choicesNameMap:
                    return Result(self.RESULT.DISH_CHOICE_NOT_FOUND, {
                        "id": dish["id"],
                        "choice": choice
                    })

                # 判断菜品选项的项目是否存在
                if option not in choicesNameMap[choice]["options"]:
                    return Result(self.RESULT.DISH_CHOICE_OPTION_NOT_FOUND, {
                        "id": dish["id"],
                        "choice": choice,
                        "option": option
                    })

            # 计算菜品的总价格
            dishTotalPrice = dish["count"] * dishInfo["price"]

            # 将菜品信息添加到菜品列表中
            dishesInfo.append({
                "id": dish["id"],
                "count": dish["count"],
                "choices": dish["choices"],
                "price": dishInfo["price"],
                "totalPrice": dishTotalPrice,
            })

            # 计算订单总金额
            totalPrice += dishTotalPrice

        # 生成订单ID
        orderUUID = uuid.uuid7()
        orderDisplayCode = uuidToShortCode(orderUUID)
        orderId = str(orderUUID)

        currentTime= datetime.datetime.now()

        # 数据库操作
        # 将总订单信息插入数据库
        self.repos.orders.insert(
            id=orderId,
            type=orderType,
            tableId=tableId if orderType == 0 else None,
            partySize=partySize,
            displayCode=orderDisplayCode,
        )


        # 将子订单信息插入到数据库
        self.repos.subOrders.insert(
            totalOrderId=orderId,
            subOrderId=1,
            note=note,
            createdAt=currentTime,
        )

        # 将订单状态信息插入到数据库
        self.repos.orderStatus.insert(
            id=orderId,
            status=0,
            createdAt=currentTime,
            creator=creatorId,
            updatedAt=currentTime,
            totalAmount=totalPrice,
        )

        # 将菜品信息插入到数据库
        for dish in dishesInfo:
            self.repos.orderItems.insert(
                orderId=orderId,
                subOrderId=1,

                dishId=dish["id"],

                price=dish["price"],
                quantity=dish["count"],

                totalPrice=dish["totalPrice"],

                choices=dish["choices"]
            )
                                        # 总订单id    子订单id

        # 提交事务
        self.repos.dishes.commit()

        return Result(self.RESULT.SUCCESS, (orderId, 1))

    def getToday(self, offset: int = 0, limit: int = 10):

        orderStatus = self.repos.orderStatus.getTodayOrders(offset, limit)


        result = {
            "unfinished": [],
            "finished": []
        }

        for statusInfo in orderStatus:

            order = self.repos.orders.get(id=statusInfo["id"])

            

            if order is None:
                # 实际上不可能抛出这个异常，除非orderStatus查到了，但是order马上被删除了
                raise ValueError()
            
            order_ = dict(order.copy())

            order_.update(statusInfo)

            if order_["status"] != 3:
                result["unfinished"].append(order_)
            else:
                result["finished"].append(order_)

        return Result(self.RESULT.SUCCESS, result)


    def _getOrderInfo(self, orderId: str, orderInfo: dict):
        if len(orderInfo) != 0:
            return
        
        row = self.repos.orders.get(id=orderId)

        if row is None:
            raise OrderNotFoundError()
        
        orderInfo.update(row)

    def _getSubOrdersInfo(self, orderId: str, subOrdersInfo: list):
        if len(subOrdersInfo) != 0:
            pass

        row = self.repos.subOrders.getAll(totalOrderId=orderId)

        subOrdersInfo.extend(row)

    def _getOrderDishesInfo(self, orderId: str, dishesInfo: list):
        if len(dishesInfo) != 0:
            pass


        row = self.repos.orderItems.getAll(orderId=orderId)

        dishesInfo.extend(row)
            
    def _getOrderStatusInfo(self, orderId: str, orderStatusInfo: dict):
        if len(orderStatusInfo) != 0:
            pass

        row = self.repos.orderStatus.get(id=orderId)

        if row is None:
            raise OrderNotFoundError()

        orderStatusInfo.update(row)
        
    def get(self, orderId: str, queries: Literal["tableName", "subOrdersCount", "dishesCount", "basicInfo"]):

        result = {}

        errors = {}

        orderInfo: _OrdersRow = cast(_OrdersRow, {})
        orderStatusInfo = {}
        subOrdersInfo: list[_SubOrdersRow] = [] 
        orderDishesInfo: list[_OrderItemsRow] = []
        
        try:
            if "tableName" in queries:

                self._getOrderInfo(orderId, orderInfo) #type: ignore
                
                shopService = ShopService(self.repos)

                if orderInfo["tableId"] is None:
                    # 当订单类型为1（外带）时，无桌台信息
                    errors["tableName"] = "NoTableInfo"

                status, data = shopService.tables.get(orderInfo["tableId"])

                result["tableName"] = data["name"] #type: ignore

            if "subOrdersCount" in queries:
                finishedCount, totalCount = 0, 0

                self._getSubOrdersInfo(orderId, subOrdersInfo)

                for subOrder in subOrdersInfo:
                    if subOrder["finishedAt"]:
                        finishedCount += 1

                    totalCount += 1

                result["subOrdersCount"] = {
                    "finished": finishedCount,
                    "total": totalCount
                }

            if "dishesCount" in queries:
                finishedCount, totalCount = 0, 0

                self._getOrderDishesInfo(orderId, orderDishesInfo)

                for dish in orderDishesInfo:
                    if dish["finishedAt"]:
                        finishedCount += 1
                    totalCount += 1

                result["dishesCount"] = {
                    "finished": finishedCount,
                    "total": totalCount
                }

            if "basicInfo" in queries:
                self._getOrderInfo(orderId, orderInfo) #type: ignore
                self._getOrderStatusInfo(orderId, orderStatusInfo)

                result_ = dict(orderInfo.copy())
                result_.update(orderStatusInfo)

                # print(result_)

                result["basicInfo"] = result_ 

        except OrderNotFoundError:
            return Result(self.RESULT.ORDER_NOT_FOUND)

        return Result(self.RESULT.SUCCESS if len(errors) == 0 else self.RESULT.HAS_PARTIAL_ERROR, {
            "result": result,
            "errors": errors 
        })
        

            
        

        

        

            




        
        