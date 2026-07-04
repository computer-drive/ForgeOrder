from typing import TypedDict

class OrderChoiceType(TypedDict):
    choice_id: int
    choice_name: str
    option_id: int
    option_name: str


class OrderItemInput(TypedDict):
    dish_id : int
    price: int
    count: int
    total_mount: int
    choices: list[OrderChoiceType]

class OrderItemRecord(OrderItemInput):
    order_id: int
    item_id: int

# 对OrderItemInput及OrderItemRecord的说明
# OrderItemInput不带order_id字段，而OrderItemRecord带order_id字段。
# 在创建新订单（调用script.main_db库中的_Orders.new方法时，传递OrderItemInput类型的数据）。
# 在内部创建时，会使用OrderItemRecord类型的数据。
# 需要注意的是，在其他地方编写类型提示时，使用OrderItemInput类型而不是OrderItemRecord类型。
