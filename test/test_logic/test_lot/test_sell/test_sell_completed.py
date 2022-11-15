from src.logic.lot.sell.sell_completed import (
    sell_act_lots_completed_in_turn,
    update_db_after_sell_of_lot,
)
from src.models import Lot, ConLot
from src.core.config import currency_pair


def test_none_sell_orders_completed_in_last_turn() -> None:
    r1 = sell_act_lots_completed_in_turn(valr_sell_lots=set(), db_sell_lots=[])
    assert r1 == set()


def test_sell_orders_completed_in_last_turn(
    mocker, test_session, test_types_lots
) -> None:
    mocker.patch("src.logic.lot.sell.sell_completed.logger.error", return_value=None)
    db_orders = test_session.query(Lot).filter(Lot.lot_status == "sell_active").all()
    r1 = sell_act_lots_completed_in_turn(valr_sell_lots=set(), db_sell_lots=db_orders)
    assert r1 == {
        108000.0,
        112000.0,
        115000.0,
        116000.0,
        111000.0,
        109000.0,
        113000.0,
        117000.0,
        110000.0,
        114000.0,
        118000.0,
        107000.0,
        119000.0,
    }
    r2 = sell_act_lots_completed_in_turn(
        valr_sell_lots={
            108000.0,
            112000.0,
            115000.0,
            116000.0,
            111000.0,
            109000.0,
            113000.0,
            117000.0,
            110000.0,
            114000.0,
            118000.0,
            107000.0,
            119000.0,
        },
        db_sell_lots=db_orders,
    )
    assert r2 == set()
    r3 = sell_act_lots_completed_in_turn(
        valr_sell_lots={
            108000.0,
            112000.0,
            115000.0,
            116000.0,
            111000.0,
            109000.0,
            113000.0,
        },
        db_sell_lots=db_orders,
    )
    assert r3 == {117000.0, 114000.0, 118000.0, 110000.0, 107000.0, 119000.0}
    r4 = sell_act_lots_completed_in_turn(
        valr_sell_lots={
            108000.0,
            112000.0,
            115000.0,
            116000.0,
            111000.0,
            109000.0,
            125000.0,
            113000.0,
        },
        db_sell_lots=db_orders,
    )
    assert r4 == {117000.0, 114000.0, 118000.0, 110000.0, 107000.0, 119000.0}


def test_update_db_after_sell_of_lot(mocker, test_session, test_types_lots) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    mocker.patch("src.adapter.utils.session", new=test_session)
    lot_price_test = 110000
    q1: Lot = (
        test_session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.lot_price == lot_price_test)
        .filter(Lot.lot_status == ConLot.sell_act)
        .one_or_none()
    )
    assert q1.price > q1.lot_price
    oq = q1.quantity
    ot = q1.amount_of_trades
    op = q1.profit_total
    update_db_after_sell_of_lot(lots_to_update={lot_price_test}, pair=currency_pair)
    q2 = (
        test_session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.lot_price == lot_price_test)
        .filter(Lot.lot_status == ConLot.sell_act)
        .one_or_none()
    )
    assert q2 is None
    q3: Lot = (
        test_session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.lot_price == lot_price_test)
        .filter(Lot.lot_status == ConLot.buy_pass)
        .one_or_none()
    )
    assert oq < q3.quantity
    assert ot + 1 == q3.amount_of_trades
    assert op < q3.profit_total
