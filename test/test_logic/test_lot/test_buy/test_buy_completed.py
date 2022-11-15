from src.logic.lot.buy.buy_completed import (
    buy_act_lots_completed_in_last_turn,
    update_db_after_buy_of_lot,
)
from src.models import Lot, ConLot
from src.core.config import currency_pair


def test_none_buy_orders_completed_in_last_turn() -> None:
    valr_orders = set()
    db_orders = []
    r1 = buy_act_lots_completed_in_last_turn(
        valr_buy_lots=valr_orders, db_buy_lots=db_orders
    )
    assert r1 == set()


def test_buy_orders_completed_in_last_turn(
    mocker, test_session, test_types_lots
) -> None:
    mocker.patch("src.logic.lot.buy.buy_completed.logger.error", return_value=None)
    db_orders = test_session.query(Lot).filter(Lot.lot_status == "buy_active").all()
    r1 = buy_act_lots_completed_in_last_turn(valr_buy_lots=set(), db_buy_lots=db_orders)
    assert r1 == {100000.0, 101000.0, 102000.0}
    r2 = buy_act_lots_completed_in_last_turn(
        valr_buy_lots={100000.0, 101000.0, 102000.0}, db_buy_lots=db_orders
    )
    assert r2 == set()
    r3 = buy_act_lots_completed_in_last_turn(
        valr_buy_lots={100000.0, 101000.0}, db_buy_lots=db_orders
    )
    assert r3 == {102000.0}
    r4 = buy_act_lots_completed_in_last_turn(
        valr_buy_lots={102000.0, 103000.0}, db_buy_lots=db_orders
    )
    assert r4 == {100000.0, 101000.0}


def test_update_db_after_buy_of_lot(mocker, test_session, test_types_lots) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    mocker.patch("src.adapter.utils.session", new=test_session)
    # update_db_after_buy_of_lot(lots_to_update=set(), pair=currency_pair)
    q1 = (
        test_session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.lot_price == 100000)
        .filter(Lot.lot_status == ConLot.buy_act)
        .one_or_none()
    )
    assert q1.lot_price == 100000.0
    assert q1.price == q1.lot_price
    update_db_after_buy_of_lot(lots_to_update={100000.0}, pair=currency_pair)
    q2 = (
        test_session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.lot_price == 100000)
        .filter(Lot.lot_status == ConLot.sell_pass)
        .one_or_none()
    )
    assert q2.price == 102000.0
