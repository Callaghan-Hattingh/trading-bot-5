from src.core.config import c_id, currency_pair, post_only, quantity, time_in_force
from src.logic.api import ValrApi
from src.models import Lot
from src.core.log import get_logger

logger = get_logger(f"{__name__}")


def gen_customer_order_id(origin_price: float, pair: str) -> str:
    return f"{c_id}{pair}{str(origin_price).replace('.', '-')}"


def filtered_open_orders(*, pair: str = currency_pair) -> list[dict]:
    oo = ValrApi.get_all_open_orders()
    foo = []
    for i in oo:
        if i["currencyPair"] == pair:
            foo.append(i)
    return foo


def post_lot_generation(price: int | float, *, side: str) -> dict:
    if currency_pair == "BTCZAR":
        price = int(price)
    data = {
        "side": side.upper(),
        "quantity": minimum_quantity_generation(price),
        "price": price,
        "pair": currency_pair,
        "postOnly": post_only,
        "customerOrderId": gen_customer_order_id(price, currency_pair),
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


def minimum_quantity_generation(price: float) -> str:
    if price * float(quantity) > 10:
        return quantity
    else:
        return f"{round(10.02 / price, 8):.8f}"


def buy_quantity_generation(
    price: float, origin_price: float, trade_quantity: float
) -> float:
    if price > origin_price:
        return trade_quantity * price / origin_price
    elif price == origin_price:
        return trade_quantity
    else:
        logger.error(f"check lot for {origin_price}, {price}, {trade_quantity}")
        return trade_quantity
