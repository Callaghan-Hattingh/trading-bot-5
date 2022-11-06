# check if any sell lots have been completed
# Get VALR open sell lots and compare with db
# Update db if sell completed
# sell active to buy passive


from src.models import Lot, ConLot
from src.core.log import get_logger
from src.adapter.lot import read_origin_price
from src.adapter.utils import commit

logger = get_logger(f"{__name__ }")


# logic errors here
def update_db_after_sell_of_lot(*, lots_to_update: set[float], pair: str) -> None:
    # calculate a change in quantity for next buy
    # add to complete trades and profit
    # change lot_status to passive_buy
    for lot in lots_to_update:
        l = read_origin_price(pair=pair, origin_price=lot)
        if l.lot_status != ConLot.sell_act:
            logger.error(f"update_db_after_buy error {l.lot_price}")
            continue
        op = l.price
        oq = l.quantity
        l.price = l.lot_price
        # l.quantity = buy_quantity_generation(
        #     price=op, lot_price=l.lot_price, trade_quantity=oq
        # )
        l.amount_of_trades += 1
        l.profit_total += l.lot_price * (l.quantity - oq)
        l.lot_status = ConLot.buy_pass
        commit()
