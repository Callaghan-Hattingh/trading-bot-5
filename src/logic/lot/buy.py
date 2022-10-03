from src.adapter.lot import create_fresh, get_origin_price, update_fresh
from src.core.config import currency_pair, max_buy_lots, step
from src.logic.api import ValrApi
from src.logic.lot.lot import batch_lot_generation, post_lot_generation


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


def check_to_place(orders: set[float]) -> list[dict]:
    """

    :param orders:
    :return:
    """
    lots = []
    for i in orders:
        q = get_origin_price(currency_pair, i)
        if not q:
            bl = post_lot_generation(i, side="BUY")
            pre_buy_db_add(bl)
            lots.append(bl)
    return lots


def pre_buy_db_add(data: dict) -> None:
    create_fresh(data)


def batch_post_buy_lots(lots: list[dict]) -> bool:
    size = 20
    batchs = [lots[x : x + size] for x in range(0, len(lots), size)]
    for b in batchs:
        bo = batch_lot_generation(b, order_type="PLACE_LIMIT")
        r = ValrApi.batch_orders(bo)
        for q, w in zip(r["outcomes"], b):
            if q["accepted"]:
                update_fresh(q["orderId"], w["price"])
            else:
                raise Exception
    return True


def buy_controller(price: float, open_orders: list[dict]):
    print(f"level 0: trade:{price}, open orders:{open_orders}")
    cpl = create_planned_lots(price)  # 1
    obl = open_buy_lots(open_orders)  # 1
    ltp = lots_to_place(obl, cpl)  # 2
    lp = lots_placed(obl, cpl)  # 2
    ctp = check_to_place(ltp)  # 3
    bpbl = batch_post_buy_lots(ctp)
