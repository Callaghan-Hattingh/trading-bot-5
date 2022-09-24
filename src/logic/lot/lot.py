from src.core.config import (c_id, currency_pair, post_only, quantity, step,
                             time_in_force)
from src.logic.api import ValrApi


def gen_customer_order_id(origin_price: int, currency_pair: str) -> str:
    return f"{c_id}{currency_pair}{origin_price}"


def filtered_open_orders(*, curency_pair: str = currency_pair, c_id: str = c_id) -> set:
    oo = ValrApi.get_all_open_orders()
    if not oo:
        return set()
    else:
        raise Exception


def post_lot_generation(price: int, *, side: str) -> dict:
    i = gen_customer_order_id(price, currency_pair)
    data = {
        "side": side.upper(),
        "quantity": quantity,
        "price": price,
        "pair": currency_pair,
        "postOnly": post_only,
        "customerOrderId": i,
        "timeInForce": time_in_force,
    }
    return data


def batch_lot_generation(
    data: list[dict], *, order_type: str
) -> list[dict[str, str | dict]]:
    reqs = []
    for _ in data:
        i = {"type": order_type, "data": _}
        reqs.append(i)
    return reqs
