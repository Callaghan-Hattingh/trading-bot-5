# check if any buy lots have been completed
# Get VALR open buy lots and compare with db
# Update db if buy completed
# buy active to sell passive
# No api calls required


from src.models import Lot, ConLot
from src.core.log import get_logger
from src.adapter.lot import read_lot_price
from src.adapter.utils import commit

logger = get_logger(f"{__name__}")


def check_for_untracked_valr_buy_act_lots(
    *, valr_lots: set[float], db_lots: set[float]
) -> None:
    # ensure that valr and db are not out of sync.
    e = valr_lots.difference(db_lots)
    if e:
        logger.error(f"check_for_untracked_valr_buy_act_lots {e}")


def buy_act_lots_completed_in_last_turn(
    *, valr_buy_lots: set[float], db_buy_lots: list[Lot]
) -> set[float]:
    db_l = set()
    for l in db_buy_lots:
        db_l.add(l.lot_price)
    check_for_untracked_valr_buy_act_lots(valr_lots=valr_buy_lots, db_lots=db_l)
    return db_l.difference(valr_buy_lots)


def update_db_after_buy_of_lot(*, lots_to_update: set[float], pair: str) -> None:
    # calculate a
    for lot in lots_to_update:
        l = read_lot_price(pair=pair, lot_price=lot, lot_status=ConLot.buy_act)
        l.price = round(l.lot_price * 1.02, 8)
        l.lot_status = ConLot.sell_pass
        commit()
