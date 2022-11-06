from datetime import datetime

from src.adapter.lot import (
    create_new,
    read_origin_price,
    update_valr_id,
    read_open_buy_orders,
    update_lot_buy,
)
from src.models import Lot

lot1 = Lot(
    origin_price=100,
    change_time=datetime.utcnow(),
    valr_id="test",
    side="BUY",
    price=100,
    quantity=0.1,
    currency_pair="BTCZAR",
    post_only=True,
    customer_order_id="test-12",
    time_in_force="GTC",
    order_status="buy_active",
)


def test_create_new(mocker, test_session) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    q1 = test_session.query(Lot).first()
    create_new(lot1)
    q2 = test_session.query(Lot).first()
    assert q1 is None
    assert q2 is not None
    assert q2.price == lot1.price
    assert q2 == lot1


def test_read_origin_price_none(test_session) -> None:
    r1 = read_origin_price("BTCZAR", 100000)
    assert r1 is None
    r2 = read_origin_price("abcxyz", 100000)
    assert r2 is None


def test_read_origin_price_one(mocker, test_session, test_default_lot) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    pair = "BTCZAR"
    price = 100000.0
    r1 = read_origin_price(pair, price)
    assert r1.origin_price == price
    assert r1.currency_pair == pair


def test_read_open_buy_orders(mocker, test_session, test_types_lots) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    r1 = read_open_buy_orders()
    assert len(r1) == 3
    assert r1[0].origin_price == 100000.0


def test_update_valr_id(mocker, test_session, test_default_lot) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    q1 = test_session.query(Lot).first()
    assert q1.valr_id == "test-1"
    update_valr_id("test-2", 100000.0)
    q2 = test_session.query(Lot).first()
    assert q2.valr_id == "test-2"


def test_update_lot_buy(mocker, test_session, test_types_lots) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    q1 = test_session.query(Lot).filter(Lot.origin_price == 120000).one()
    assert q1.valr_id == "test-2"
    assert q1.order_status == "sell_passive"
    update_lot_buy(q1)
    q2 = test_session.query(Lot).filter(Lot.origin_price == 120000).one()
    assert q2.valr_id == "valr_id"
    assert q2.order_status == "buy_active"
