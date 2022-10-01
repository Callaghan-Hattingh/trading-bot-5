from datetime import datetime

from dateutil import parser

from src.db.base import session
from src.models import Trade


def create(data):
    trade = Trade(
        change_time=datetime.utcnow(),
        valr_id=data["valr_id"],
        price=data["price"],
        quantity=data["quantity"],
        currency_pair=data["currency_pair"],
        traded_at=parser.parse(data["traded_at"]),
        taker_side=data["taker_side"],
        sequence_id=data["sequence_id"],
        quote_volume=data["quote_volume"],
    )
    session.add(trade)
    session.commit()
