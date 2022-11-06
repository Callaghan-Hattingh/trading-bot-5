# check if any buy orders have been completed
# Get VALR open buy orders and compare with db
# Update db if buy completed
# from src.logic.lot.utils import open_orders_type
# from src.adapter.lot import read_open_buy_orders
from src.models import Lot, ConLot
from src.core.log import get_logger
from src.adapter.lot import read_origin_price
from src.logic.lot.utils import buy_quantity_generation
from src.adapter.utils import commit

logger = get_logger(f"{__name__ }")


def check_for_untracked_valr_act_buy_lots(
    *, valr_orders: set[float], db_lots: set[float]
) -> None:
    # ensure that valr and db are not out of sync.
    e = valr_orders.difference(db_lots)
    if e:
        logger.error(f"buy_orders_completed_in_last_turn {e}")


def buy_orders_completed_in_last_turn(
    *, valr_orders: set[float], db_lots: list[Lot]
) -> set[float]:
    db_l = set()
    for o in db_lots:
        db_l.add(o.origin_price)
    check_for_untracked_valr_act_buy_lots(valr_orders=valr_orders, db_lots=db_l)
    return db_l.difference(valr_orders)


def update_db_after_buy(*, lots_to_update: set[float], pair: str) -> None:
    # calculate a change in quantity for next buy
    # add to complete trades and profit
    # change order_status to passive_buy
    for lot in lots_to_update:
        l = read_origin_price(pair=pair, origin_price=lot)
        if l.order_status != ConLot.sell_act:
            logger.error("")
            continue
        op = l.price
        oq = l.quantity
        l.price = l.origin_price
        l.quantity = buy_quantity_generation(
            price=op, origin_price=l.origin_price, trade_quantity=oq
        )
        l.amount_of_trades += 1
        l.profit_total += l.origin_price * (l.quantity - oq)
        l.order_status = ConLot.buy_pass
        commit()
