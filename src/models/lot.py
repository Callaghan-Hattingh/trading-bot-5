# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql.expression import text
from datetime import datetime
from test.conftest import TestingSessionLocal

from factory import LazyFunction, Sequence, alchemy, fuzzy
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


# Exchange or Deal
class Lot(Base):
    __tablename__ = "lot"

    id = Column(Integer, primary_key=True, nullable=False)
    origin_price = Column(Float, nullable=False, index=True, unique=True)
    change_time = Column(TIMESTAMP(timezone=True), nullable=False)
    valr_id = Column(String(36), nullable=False)  # UUID
    side = Column(Enum("BUY", "SELL", names="side"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    post_only = Column(Boolean, nullable=False)
    customer_order_id = Column(String(50), nullable=False)
    time_in_force = Column(
        Enum("GTC", "FOK", "IOC", names="time_in_force"), nullable=False
    )
    order_status = Column(
        Enum(
            "neutral",
            "buy_active",
            "buy_passive",
            "sell_active",
            "sell_passive",
            "error",
            names="order_status",
        ),
        nullable=False,
    )
    profit_total = Column(Float, nullable=False, default=0)
    amount_of_trades = Column(Integer, nullable=False, default=0)
    fee_currency_zar = Column(Float, nullable=False, default=0)
    fee_currency_crypto = Column(Float, nullable=False, default=0)


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
        ["neutral", "buy_active", "buy_passive", "sell_active", "sell_passive"]
    )
    profit_total = fuzzy.FuzzyFloat(10000000)
    amount_of_trades = fuzzy.FuzzyInteger(100)
    fee_currency_zar = fuzzy.FuzzyFloat(100)
    fee_currency_crypto = fuzzy.FuzzyFloat(100)

    class Meta:
        model = Lot
        sqlalchemy_session = TestingSessionLocal
