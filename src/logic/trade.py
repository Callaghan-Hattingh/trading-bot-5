from src.adapter.trade import create
from src.logic.api import ValrApi
from src.core.config import correction_number


def last_amount_traded():
    r = ValrApi.get_trade_hist(pair="BTCZAR", skip=0, limit=1)[0]
    data = {
        "price": r["price"],
        "quantity": r["quantity"],
        "currency_pair": r["currencyPair"],
        "traded_at": r["tradedAt"],
        "taker_side": r["takerSide"],
        "sequence_id": r["sequenceId"],
        "valr_id": r["id"],
        "quote_volume": r["quoteVolume"],
    }
    create(data)
    return int(r["price"]) - correction_number
