from src.adapter.lot import get_origin_price
from src.core.config import currency_pair, max_buy_orders, step, quantity, post_only, time_in_force
from src.logic.lot.lot import gen_customer_order_id


def live_orders(price: int) -> set[int]:
    s = set()
    max_s = (price - 1) // step * step
    for _ in range(1, max_buy_orders + 1):
        s.add(max_s - step * _)
    return s


def check_open_orders_to_place(
    open_orders: set[int], planned_orders: set[int]
) -> set[int]:
    return planned_orders.difference(open_orders)


def check_open_orders_placed(
    open_orders: set[int], planned_orders: set[int]
) -> set[int]:
    return open_orders.difference(planned_orders)


def check_db_to_place(orders: set[int]) -> set[int]:
    for i in orders:
        q = get_origin_price(currency_pair, i)
        if not q:
            print("klkjl")
    return orders


def buy_order_generation(price: int) -> dict:
    print(price)
    i = gen_customer_order_id(price, currency_pair)
    print(i)
    data = {
        "side": "BUY",
        "quantity": quantity,
        "price": price,
        "pair": currency_pair,
        "postOnly": post_only,
        "customerOrderId": i,
        "timeInForce": time_in_force,
    }
    print(data)


def buy_orders_to_be_posted(possible_buys: set) -> set:
    # if an open buy lot is lower than buy_min -> cancel
    # set of orders to be cancelled

    # post to valr

    # update d
    pass


def buy_controller(price):
    pb = live_orders(price)
    i = set()
    print(pb)
    pb = check_open_orders_to_place(i, pb)
    print(pb)
    cb = check_open_orders_placed(i, pb)
    print(cb)
    pb = check_db_to_place(pb)
    print(buy_order_generation(34334342))
