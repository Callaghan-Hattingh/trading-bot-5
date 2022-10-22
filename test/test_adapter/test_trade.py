from datetime import datetime

from src.adapter.trade import create
from src.models import Trade

trade1 = Trade(
    change_time=datetime.utcnow(),
    valr_id="test-trade-1",
    price=100000,
    quantity=0.1,
    currency_pair="BTCZAR",
    traded_at=datetime.utcnow(),
    taker_side="buy",
    sequence_id=137874433455,
    quote_volume=0.2,
)


def test_create(mocker, test_session) -> None:
    mocker.patch("src.adapter.trade.session", new=test_session)
    q1 = test_session.query(Trade).first()
    create(trade1)
    q2 = test_session.query(Trade).first()
    assert q1 is None
    assert q2 is not None
    assert q2.price == trade1.price
    assert q2 == trade1
