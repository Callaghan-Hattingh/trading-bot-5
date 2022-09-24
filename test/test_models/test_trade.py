from src.models import Trade, TradeFactory


def test_trade(test_session):
    q = test_session.query(Trade).all()
    assert q == []
    TradeFactory.create()
    q = test_session.query(Trade).all()
    assert q != []


def test_trade_adapter(test_session):
    data = {
        "price": "240000",
        "quantity": "0.19052818",
        "currencyPair": "BTCZAR",
        "tradedAt": "2020-11-30T08:55:29.338087Z",
        "takerSide": "buy",
        "sequenceId": 15828,
        "id": "b01709e5-31d0-4d15-a5a6-3fd7d18d4e64",
        "quoteVolume": "45726.7632",
    }
