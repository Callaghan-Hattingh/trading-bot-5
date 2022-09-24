from src.core.config import c_id, step
from src.logic.api import ValrApi


def gen_customer_order_id(origin_price: int, currency_pair: str) -> str:
    return f"{c_id}{currency_pair}{origin_price}"


def filtered_open_orders(curency_pair: str) -> set:
    r = ValrApi.get_all_open_orders()
    print(r)
    return set(r)




