from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

from src.db.base import Base


@dataclass
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
            "buy_passive",
            "buy_active",
            "sell_active",
            "sell_passive",
            "error",
            names="order_status",
        ),
        nullable=False,
    )
    profit_total = Column(Float, nullable=False, default=0)
    amount_of_trades = Column(Integer, nullable=False, default=0)
    batchId = Column(Integer, nullable=False, default=-1)
    fee_currency_zar = Column(Float, nullable=False, default=0)
    fee_currency_crypto = Column(Float, nullable=False, default=0)


@dataclass
class ConLot:
    bzar = "BTCZAR"
    ezar = "ETHZAR"
    xzar = "XRPZAR"
    buy = "BUY"
    sell = "SELL"
    buy_pass = "buy_passive"
    buy_act = "buy_active"
    sell_act = "sell_active"
    sell_pass = "sell_passive"
    err = "error"
