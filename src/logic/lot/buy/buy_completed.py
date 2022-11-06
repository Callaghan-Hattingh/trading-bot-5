# check if any buy lots have been completed
# Get VALR open buy lots and compare with db
# Update db if buy completed
# buy active to sell passive


from src.models import Lot, ConLot
from src.core.log import get_logger
from src.adapter.lot import read_origin_price
from src.logic.lot.utils import buy_quantity_generation
from src.adapter.utils import commit

logger = get_logger(f"{__name__}")


def check_for_untracked_valr_act_buy_lots(
        *, valr_lots: set[float], db_lots: set[float]
) -> None:
    # ensure that valr and db are not out of sync.
    e = valr_lots.difference(db_lots)
    if e:
        logger.error(f"buy_orders_completed_in_last_turn {e}")


def buy_act_lots_completed_in_last_turn(
        *, valr_buy_lots: set[float], db_buy_lots: list[Lot]
) -> set[float]:
    db_l = set()
    for o in db_buy_lots:
        db_l.add(o.lot_price)
    check_for_untracked_valr_act_buy_lots(valr_lots=valr_buy_lots, db_lots=db_l)
    return db_l.difference(valr_buy_lots)


# logic errors here
def update_db_after_buy_of_lot(*, lots_to_update: set[float], pair: str) -> None:
    # calculate a change in quantity for next buy
    # add to complete trades and profit
    # change lot_status from buy_active to sell_passive
    for lot in lots_to_update:
        l = read_origin_price(pair=pair, origin_price=lot)
        if l.lot_status != ConLot.buy_act:
            logger.error(f"update_db_after_buy_of_lot error {l.lot_price}")
            continue
        op = l.price
        oq = l.quantity
        l.price = l.lot_price
        l.quantity = buy_quantity_generation(
            price=op, origin_price=l.lot_price, trade_quantity=oq
        )
        l.amount_of_trades += 1
        l.profit_total += l.lot_price * (l.quantity - oq)
        l.lot_status = ConLot.buy_pass
        commit()
