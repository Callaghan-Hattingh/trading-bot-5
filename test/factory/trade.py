from test.conftest import TestingSessionLocal
from src.models.trade import Trade
from datetime import datetime

from factory import LazyFunction, Sequence, alchemy, fuzzy


class TradeFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: "%s" % n)
    change_time = LazyFunction(datetime.utcnow)
    valr_id = fuzzy.FuzzyText(length=36)
    taker_side = fuzzy.FuzzyChoice(["BUY", "SELL"])
    price = fuzzy.FuzzyFloat(10000000)
    quantity = fuzzy.FuzzyFloat(100)
    currency_pair = fuzzy.FuzzyChoice(["BTCZAR", "ETHZAR", "XRPZAR"])
    traded_at = LazyFunction(datetime.utcnow)
    sequence_id = fuzzy.FuzzyInteger(1018518407588352000)
    quote_volume = fuzzy.FuzzyFloat(100)

    class Meta:
        model = Trade
        sqlalchemy_session = TestingSessionLocal
