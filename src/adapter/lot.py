from datetime import datetime

from src.core.config import currency_pair
from src.db.base import session
from src.models import Lot


def get_open_orders_from_db(currency_pair: str):
    q = session.query(Lot).filter(Lot.currency_pair == currency_pair).all()
    return q


def get_origin_price(currency_pair: str, origin_price: int):
    q = (
        session.query(Lot)
        .filter(Lot.currency_pair == currency_pair)
        .filter(Lot.origin_price == origin_price)
        .all()
    )
    return q


def create_fresh(data):
    """
    valr_id = fresh_buy
    order_status = buy_active
    :param data: data for lot
    :return: None
    """
    lot = Lot(
        origin_price=data["price"],
        change_time=datetime.utcnow(),
        valr_id="fresh_buy",
        side=data["side"],
        price=data["price"],
        quantity=data["quantity"],
        currency_pair=currency_pair,
        post_only=data["postOnly"],
        customer_order_id=data["customerOrderId"],
        time_in_force=data["timeInForce"],
        order_status="buy_active",
    )
    session.add(lot)
    session.commit()


def update_fresh(valr_id: str, price: int):
    session.query(Lot).filter(Lot.origin_price == price).update({"valr_id": valr_id})
    session.commit()
