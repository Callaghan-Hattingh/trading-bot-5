# check if any sell lots have been completed
# Get VALR open sell lots and compare with db
# Update db if sell completed
# sell active to buy passive


from src.models import Lot, ConLot
from src.core.log import get_logger
from src.adapter.lot import read_lot_price
from src.adapter.utils import commit
from src.logic.lot.utils import buy_pass_quantity_generation

logger = get_logger(f"{__name__}")


def check_for_untracked_valr_sell_act_lots(
    *, valr_lots: set[float], db_lots: set[float]
) -> None:
    # ensure that valr and db are not out of sync.
    e = valr_lots.difference(db_lots)
    if e:
        logger.error(f"check_for_untracked_valr_sell_act_lots {e}")


def sell_act_lots_completed_in_turn(
    *, valr_sell_lots: set[float], db_sell_lots: list[Lot]
) -> set[float]:
    db_l = set()
    for l in db_sell_lots:
        db_l.add(l.lot_price)
    check_for_untracked_valr_sell_act_lots(valr_lots=valr_sell_lots, db_lots=db_l)
    return db_l.difference(valr_sell_lots)


def update_db_after_sell_of_lot(*, lots_to_update: set[float], pair: str) -> None:
    # calculate a change in quantity for next buy
    # add to complete trades and profit
    # change lot_status from sell_act to buy_pass
    for lot in lots_to_update:
        l = read_lot_price(pair=pair, lot_price=lot, lot_status=ConLot.sell_act)
        op = l.price
        oq = l.quantity
        l.price = l.lot_price
        l.quantity = buy_pass_quantity_generation(
            price=op, lot_price=l.lot_price, trade_quantity=oq
        )
        l.amount_of_trades += 1
        l.profit_total += (op - l.price) * (oq * l.price / op)
        l.lot_status = ConLot.buy_pass
        commit()
