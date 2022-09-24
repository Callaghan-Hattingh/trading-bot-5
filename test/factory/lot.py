from test.conftest import TestingSessionLocal
from src.models.lot import Lot
from datetime import datetime

from factory import LazyFunction, Sequence, alchemy, fuzzy


class LotFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: "%s" % n)
    change_time = LazyFunction(datetime.utcnow)
    valr_id = fuzzy.FuzzyText(length=36)
    side = fuzzy.FuzzyChoice(["BUY", "SELL"])
    price = fuzzy.FuzzyFloat(10000000)
    quantity = fuzzy.FuzzyFloat(100)
    currency_pair = fuzzy.FuzzyChoice(["BTCZAR", "ETHZAR", "XRPZAR"])
    post_only = fuzzy.FuzzyChoice([True, False])
    customer_order_id = fuzzy.FuzzyText(length=50)
    time_in_force = fuzzy.FuzzyChoice(["GTC", "FOK", "IOC"])
    order_status = fuzzy.FuzzyChoice(
        ["neutral", "buy_active", "sell_active", "sell_passive"]
    )
    profit_total = fuzzy.FuzzyFloat(10000000)
    amount_of_trades = fuzzy.FuzzyInteger(100)
    fee_currency_zar = fuzzy.FuzzyFloat(100)
    fee_currency_crypto = fuzzy.FuzzyFloat(100)

    class Meta:
        model = Lot
        sqlalchemy_session = TestingSessionLocal
