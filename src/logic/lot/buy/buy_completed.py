# check if any buy orders have been completed
# Get VALR open buy orders and compare with db
# Update db if buy completed
from src.logic.lot.utils import open_orders_type
from src.adapter.lot import get_open_buy_orders
from src.models import Lot
from src.core.log import get_logger

logger = get_logger(f"{__name__ }")

valr_open_buy_orders = open_orders_type()
db_open_db_orders = get_open_buy_orders()


def buy_orders_completed_in_last_turn(*, valr_orders: set[float], db_orders: list[Lot]) -> set[float]:
    db_o = set()
    for o in db_orders:
        db_o.add(o.price)
        # print(o)

    # ensure that valr and db are not out of sync.
    e = valr_orders.difference(db_o)
    if e:
        logger.error(f"buy_orders_completed_in_last_turn {e}")

    return db_o.difference(valr_orders)


def update_db_after_buy() -> None:
    pass



