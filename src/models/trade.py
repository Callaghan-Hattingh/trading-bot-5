# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql.expression import text
from datetime import datetime
from test.conftest import TestingSessionLocal

from factory import LazyFunction, Sequence, alchemy, fuzzy
from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, nullable=False)
    # change_time = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )
    change_time = Column(TIMESTAMP(timezone=True), nullable=False)
    # valr_id = Column(UUID(as_uuid=True), nullable=False)  # UUID
    valr_id = Column(String(36), nullable=False)  # UUID
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    traded_at = Column(TIMESTAMP, nullable=False)
    taker_side = Column(Enum("BUY", "SELL", names="side"), nullable=False)
    sequence_id = Column(Integer, nullable=False)
    quote_volume = Column(Float, nullable=False)


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
