# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql.expression import text
from datetime import datetime
from test.conftest import TestingSessionLocal

from factory import LazyFunction, Sequence, alchemy, fuzzy
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, nullable=False)
    # change_time = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )
    change_time = Column(TIMESTAMP(timezone=True), nullable=False)
    # valr_id = Column(UUID(as_uuid=True), nullable=False)  # UUID
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
            "empty",
            "buy_alive",
            "buy_dead",
            "sell_alive",
            "sell_dead",
            names="order_status",
        ),
        nullable=False,
    )


class OrderFactory(alchemy.SQLAlchemyModelFactory):
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
        ["empty", "buy_alive", "buy_dead", "sell_alive", "sell_dead", "error"]
    )

    class Meta:
        model = Order
        sqlalchemy_session = TestingSessionLocal
