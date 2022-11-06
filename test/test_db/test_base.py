from sqlalchemy import create_engine

from src.db.base import create_tables
from src.models import Lot


def test_create_tables(mocker, test_session, test_default_lot):
    mocker.patch(
        "src.db.base.engine", new=create_engine("sqlite:///test_sqlite.db", echo=False)
    )
    q1 = test_session.query(Lot).all()
    assert q1[0].valr_id == "test-1"
    test_session.commit()
    create_tables()
    q2 = test_session.query(Lot).all()
    assert q2 == []
