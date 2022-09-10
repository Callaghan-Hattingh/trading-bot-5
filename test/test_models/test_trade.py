from src.models import Trade, TradeFactory


def test_trade(session):
    q = session.query(Trade).all()
    assert q == []
    TradeFactory.create()
    q = session.query(Trade).all()
    assert q != []
