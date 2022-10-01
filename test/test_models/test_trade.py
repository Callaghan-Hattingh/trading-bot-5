from test.factory.trade import TradeFactory

from src.models import Trade


def test_trade(test_session):
    q = test_session.query(Trade).all()
    assert q == []
    TradeFactory.create()
    q = test_session.query(Trade).all()
    assert q != []
