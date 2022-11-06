from datetime import datetime

from src.adapter.lot import (
    create_new,
    read_origin_price,
    update_valr_id,
    update_lot_buy,
)
from src.core.config import currency_pair, max_buy_lots, step
from src.core.log import get_logger
from src.logic.api import batch_orders
from src.logic.lot.utils import (
    batch_lot_generation,
    post_lot_generation,
    post_lot_payload,
    open_orders_type,
)
from src.models import ConLot, Lot, ConTrade

logger = get_logger(f"{__name__}")


def create_planned_lots(price: float) -> set[float]:
    """
    To create the set of buy lots that should exist.
    :param price: last traded price
    :return: set of buy prices to be placed
    """
    s = set()
    max_s = (price - 1) // step * step
    for _ in range(1, max_buy_lots + 1):
        s.add(max_s - step * _)
    return s


def lots_to_place(placed_lots: set[float], planned_lots: set[float]) -> set[float]:
    """
    Calculate the lots to be placed
    :param placed_lots: the lots already placed
    :param planned_lots: the lots planned to exist
    :return: the lots to be created
    """
    return planned_lots.difference(placed_lots)


def lots_placed_to_be_cancelled(
    placed_lots: set[float], planned_lots: set[float]
) -> set[float]:
    """
    Calculate which of the activate lots are to be cancelled
    :param placed_lots: the lots already placed
    :param planned_lots: the lots planned to exist
    :return: the open buy lots to be cancelled
    """
    s = set()
    m = min(planned_lots)
    for _ in placed_lots:
        if _ < m:
            s.add(_)
    return s


def check_to_place(orders: set[float]) -> list[dict]:
    lots = []
    for i in orders:
        buy = read_origin_price(currency_pair, i)
        if not buy:
            bl = post_lot_generation(i, side=ConLot.buy)
            pre_buy_db_add(bl)
            lots.append(bl)
        elif buy.order_status == ConLot.buy_pass:
            bl = post_lot_payload(buy)
            update_lot_buy(buy)
            lots.append(bl)
    return lots


def pre_buy_db_add(data: dict) -> None:
    lot = Lot(
        origin_price=data["price"],
        change_time=datetime.utcnow(),
        valr_id="fresh_buy",
        side=data["side"],
        quantity=data["quantity"],
        price=data["price"],
        currency_pair=data["pair"],
        post_only=data["postOnly"],
        customer_order_id=data["customerOrderId"],
        time_in_force=data["timeInForce"],
        order_status=ConLot.buy_act,
    )
    create_new(lot)


def batch_post_buy_lots(lots: list[dict]) -> bool:
    size = 20
    batches = [lots[x : x + size] for x in range(0, len(lots), size)]
    for b in batches:
        bo = batch_lot_generation(b, order_type="PLACE_LIMIT")
        r = batch_orders(bo)
        for q, w in zip(r["outcomes"], b):
            if q["accepted"]:
                update_valr_id(q["orderId"], w["price"])
            else:
                raise Exception
    return True


def buy_controller(price: float, open_orders: list[dict]):
    print(f"level 0: trade:{price}, open orders:{open_orders}")
    cpl = create_planned_lots(price)  # 1
    obl = open_orders_type(open_orders=open_orders, side_type=ConTrade.buy)
    ltp = lots_to_place(obl, cpl)  # 2
    # lp = lots_placed(obl, cpl)  # 2
    ctp = check_to_place(ltp)  # 3
    bpbl = batch_post_buy_lots(ctp)
