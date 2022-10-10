from src.adapter.lot import get_origin_price, create_new, update_valr_id
from src.models import Lot
from datetime import datetime

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


def test_get_origin_price_none(test_session) -> None:
    r1 = get_origin_price("BTCZAR", 100000)
    assert r1 is None
    r2 = get_origin_price("abcxyz", 100000)
    assert r2 is None


def test_get_origin_price_one(mocker, test_session, test_lot) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    pair = "BTCZAR"
    price = 100000.0
    r1 = get_origin_price(pair, price)
    assert r1.origin_price == price
    assert r1.currency_pair == pair


def test_create_new(mocker, test_session) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    q1 = test_session.query(Lot).first()
    create_new(lot1)
    q2 = test_session.query(Lot).first()
    assert q1 is None
    assert q2 is not None
    assert q2.price == lot1.price
    assert q2 == lot1


def test_update_valr_id(mocker, test_session, test_lot) -> None:
    mocker.patch("src.adapter.lot.session", new=test_session)
    q1 = test_session.query(Lot).first()
    assert q1.valr_id == "test-1"
    update_valr_id("test-2", 100000.0)
    q2 = test_session.query(Lot).first()
    assert q2.valr_id == "test-2"
