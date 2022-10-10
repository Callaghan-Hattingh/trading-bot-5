from src.db.base import session
from src.models import Trade


def create(trade: Trade) -> None:
    session.add(trade)
    session.commit()
