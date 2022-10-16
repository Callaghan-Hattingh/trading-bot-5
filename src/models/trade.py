from sqlalchemy import BigInteger, Column, Enum, Float, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from dataclasses import dataclass
from src.db.base import Base


@dataclass
class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, nullable=False)
    change_time = Column(TIMESTAMP(timezone=True), nullable=False)
    valr_id = Column(String(36), nullable=False)  # UUID
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    currency_pair = Column(
        Enum("BTCZAR", "ETHZAR", "XRPZAR", names="currency_pair"), nullable=False
    )
    traded_at = Column(TIMESTAMP, nullable=False)
    taker_side = Column(Enum("buy", "sell", names="side"), nullable=False)
    sequence_id = Column(BigInteger, nullable=False)
    quote_volume = Column(Float, nullable=False)


@dataclass
class ConTrade:
    bzar = "BTCZAR"
    ezar = "ETHZAR"
    xzar = "XRPZAR"
    buy = "buy"
    sell = "sell"
