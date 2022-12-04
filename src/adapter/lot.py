from src.db.base import session
from src.models import Lot, ConLot
from uuid import UUID
from src.core.config import currency_pair


def create_new(lot: Lot) -> None:
    session.add(lot)
    session.commit()


def read_lot_price(pair: str, lot_price: float, lot_status: str) -> Lot | None:
    return (
        session.query(Lot)
        .filter(Lot.currency_pair == pair)
        .filter(Lot.lot_price == lot_price)
        .filter(Lot.lot_status == lot_status)
        .one_or_none()
    )


def read_open_buy_act_lots() -> list[Lot]:
    return session.query(Lot).filter(Lot.lot_status == ConLot.buy_act).all()


def read_lot_id_of_buy_act(*, lot_price: float) -> str:
    return (
        session.query(Lot)
        .filter(Lot.lot_price == lot_price)
        .filter(Lot.lot_status == ConLot.buy_act)
        .filter(Lot.currency_pair == currency_pair)
        .with_entities(Lot.valr_id)
        .one()
    )


def update_valr_id(valr_id: str, price: float) -> None:
    session.query(Lot).filter(Lot.lot_price == price).update({"valr_id": valr_id})
    session.commit()


def update_lot_buy(lot: Lot) -> None:
    lot.valr_id = "valr_id"
    lot.lot_status = ConLot.buy_act
    session.commit()
