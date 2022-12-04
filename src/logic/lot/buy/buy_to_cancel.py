# check if any buy lots should be cancelled
# Get VALR open buy lots and compare with amount of buy trades and last trade price
# Update db if buy cancelled
# buy active to buy passive
# buy cancel api call


from src.adapter.lot import (
    read_lot_id_of_buy_act,
)
from src.core.config import (
    currency_pair,
    max_buy_lots,
    step,
    batch_cancel_type,
    batch_lot_size,
)
from src.core.log import get_logger
from src.logic.api import batch_orders

logger = get_logger(f"{__name__}")


def list_of_planned_buy_act_lots(*, price: float) -> set[float]:
    """
    To create the set of buy active lots that should exist.
    :param price: last traded price
    :return: set of buy prices to be placed
    """
    s = set()
    max_s = (price - 1) // step * step
    for _ in range(0, max_buy_lots):
        s.add(max_s - step * _)
    return s


def list_of_planned_buy_act_to_buy_pass_lots(
    *, placed_buy_act: set[float], planned_buy_act: set[float]
) -> set[float]:
    """
    Calculate which of the activate lots are to be cancelled
    :param placed_buy_act: the lots already placed
    :param planned_buy_act: the lots planned to exist
    :return: the open buy lots to be cancelled
    """
    return placed_buy_act.difference(planned_buy_act)


# first do api request
def create_cancel_lots_batch_buy_act_to_buy_pass(
    *,
    buy_act_lots_to_cancel: set[float],
) -> list[dict]:
    """
    [
        {
            "type": "CANCEL_ORDER",
            "data": {
                "orderId":"e5886f2d-191b-4330-a221-c7b41b0bc553",
                "pair": "ETHZAR"
            }
        }
    ]
    :param buy_act_lots_to_cancel:
    :return:
    """
    batch = []
    for lot in buy_act_lots_to_cancel:
        valr_id = read_lot_id_of_buy_act(lot_price=lot)
        batch.append(
            {
                "type": batch_cancel_type,
                "data": {"orderId": valr_id, "pair": currency_pair},
            }
        )
    return batch


# need to check and ensure lot cancel order feedback/reporting
# need to do an integration once off test. with three orders
def send_batch_cancellation_of_buy_act(buy_act_batch_lots: list[dict]) -> list[dict]:
    outcomes = []
    batches = [
        buy_act_batch_lots[x : x + batch_lot_size]
        for x in range(0, len(buy_act_batch_lots), batch_lot_size)
    ]
    for batch in batches:
        resp = batch_orders(batch)
        outcomes.append(resp.json().get("outcomes"))
    return outcomes


# second update db on successful cancel of order
def update_db_for_buy_act_to_buy_pass(buy_act_lots_cancelled: set[float]) -> None:
    pass
