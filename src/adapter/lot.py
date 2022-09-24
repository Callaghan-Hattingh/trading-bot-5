from src.db.base import session
from src.models import Lot


def create(data):
    order = Lot()
    session.add(order)
    session.commit()


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
