from src.logic.lot.buy.buy_completed import (
    buy_orders_completed_in_last_turn,
    update_db_after_buy,
)
from src.models import Lot, ConLot
from src.core.config import currency_pair


def test_none_buy_orders_completed_in_last_turn() -> None:
    valr_orders = set()
    db_orders = []
    r1 = buy_orders_completed_in_last_turn(valr_orders=valr_orders, db_lots=db_orders)
    assert r1 == set()


def test_buy_orders_completed_in_last_turn(
    mocker, test_session, test_types_lots
) -> None:
    mocker.patch("src.logic.lot.buy.buy_completed.logger.error", return_value=None)
    db_orders = test_session.query(Lot).filter(Lot.order_status == "buy_active").all()
    r1 = buy_orders_completed_in_last_turn(valr_orders=set(), db_lots=db_orders)
    assert r1 == {100000.0, 101000.0, 102000.0}
    r2 = buy_orders_completed_in_last_turn(
        valr_orders={100000.0, 101000.0, 102000.0}, db_lots=db_orders
    )
    assert r2 == set()
    r3 = buy_orders_completed_in_last_turn(
        valr_orders={100000.0, 101000.0}, db_lots=db_orders
    )
    assert r3 == {102000.0}
    r4 = buy_orders_completed_in_last_turn(
        valr_orders={102000.0, 103000.0}, db_lots=db_orders
    )
    assert r4 == {100000.0, 101000.0}


def test_update_db_after_buy(mocker, test_session, test_types_lots) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    origin_price_test = 107000
    q1: Lot = test_session.query(Lot).filter(Lot.origin_price == origin_price_test).one()
    q1q = q1.quantity
    q1t = q1.amount_of_trades
    assert q1.price > q1.origin_price
    update_db_after_buy(
        lots_to_update={origin_price_test}, pair=currency_pair
    )
    q2: Lot = test_session.query(Lot).filter(Lot.origin_price == origin_price_test).one()
    assert q2.price == q1.origin_price == q2.origin_price
    assert q2.quantity > q1q
    assert q2.order_status == ConLot.buy_pass
    assert q2.amount_of_trades == q1t + 1
