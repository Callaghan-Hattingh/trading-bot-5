from datetime import datetime

from src.adapter.lot import create_new, get_origin_price, update_valr_id
from src.core.config import currency_pair, max_buy_lots, step
from src.core.log import get_logger
from src.logic.api import batch_orders
from src.logic.lot.lot import (
    batch_lot_generation,
    buy_quantity_generation,
    post_lot_generation,
)
from src.models import ConLot, Lot

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


def open_buy_lots(open_orders: list[dict]) -> set[float]:
    """
    Filter the open orders to only include buy side orders
    :param open_orders: open orders
    :return: buy open orders
    """
    o = set()
    for i in open_orders:
        # open orders side is lowercase
        if i["side"] == "buy":
            o.add(float(i["price"]))
    return o


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


def neutral_buy_order_status(buy: Lot) -> dict:
    # change to return a db instead
    op = buy.price
    oq = buy.quantity
    # place a buy
    buy.valr_id = "fresh_buy"
    buy.side = ConLot.buy
    buy.price = buy.origin_price
    buy.quantity = buy_quantity_generation(op, buy.origin_price, oq)
    buy.order_status = ConLot.buy_act
    return buy


def sell_act_buy_order_status(buy: Lot) -> dict:
    buy = neutral_buy_order_status(buy)
    buy.amount_of_trades = buy.amount_of_trades + 1
    return buy


def check_to_place(orders: set[float]) -> list[dict]:
    lots = []
    for i in orders:
        buy = get_origin_price(currency_pair, i)
        if not buy:
            bl = post_lot_generation(i, side=ConLot.buy)
            pre_buy_db_add(bl)
            lots.append(bl)
        # check different order status
        elif buy.order_status == ConLot.neu:
            bl = neutral_buy_order_status(buy)
            # db lot update
            lots.append(bl)

        elif buy.order_status == ConLot.buy_act:
            # a possible buy has been done
            # logger.warning(f"")
            # place a sale order
            pass
        elif buy.order_status == ConLot.sell_act:
            # a possible sell has been done
            # calculate a new quantity
            bl = sell_act_buy_order_status(buy)

            pass
        elif buy.order_status == ConLot.sell_pass:
            # either a massive jump in price
            # place a sell order
            pass
        else:
            # log error
            logger.warning(f"error on check_to_place for {buy.origin_price}")
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
    obl = open_buy_lots(open_orders)  # 1
    ltp = lots_to_place(obl, cpl)  # 2
    # lp = lots_placed(obl, cpl)  # 2
    ctp = check_to_place(ltp)  # 3
    bpbl = batch_post_buy_lots(ctp)
