from src.db.base import session
from src.models import Lot, ConLot


def create_new(lot: Lot) -> None:
    session.add(lot)
    session.commit()


def read_origin_price(pair: str, origin_price: float) -> Lot | None:
    return (
        session.query(Lot)
        .filter(Lot.currency_pair == pair)
        .filter(Lot.origin_price == origin_price)
        .one_or_none()
    )


def read_open_buy_orders() -> list[Lot]:
    return session.query(Lot).filter(Lot.order_status == ConLot.buy_act).all()


def update_valr_id(valr_id: str, price: float) -> None:
    session.query(Lot).filter(Lot.origin_price == price).update({"valr_id": valr_id})
    session.commit()


def update_lot_buy(lot: Lot) -> None:
    lot.valr_id = "valr_id"
    lot.order_status = ConLot.buy_act
    session.commit()
