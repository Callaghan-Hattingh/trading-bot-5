from datetime import datetime

from dateutil import parser

from src.adapter.trade import create
from src.core.config import correction_number
from src.logic.api import get_trade_hist
from src.models import ConTrade, Trade


def last_amount_traded() -> float:
    r = get_trade_hist(pair=ConTrade.bzar, skip=0, limit=1)[0]
    trade = Trade(
        price=r["price"],
        quantity=r["quantity"],
        currency_pair=r["currencyPair"],
        traded_at=parser.parse(r["tradedAt"]),
        taker_side=r["takerSide"],
        sequence_id=r["sequenceId"],
        valr_id=r["id"],
        quote_volume=r["quoteVolume"],
        change_time=datetime.utcnow(),
    )
    create(trade)
    return float(r["price"]) - correction_number
