from src.models import Lot
from test.factory.lot import LotFactory


def test_lot(test_session):
    q = test_session.query(Lot).all()
    assert q == []
    LotFactory.create()
    q = test_session.query(Lot).all()
    assert q != []
