import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# from test.factory.lot import LotFactory
from src.db.base import Base

engine = create_engine("sqlite:///test_sqlite.db", echo=False)
TestingSessionLocal = scoped_session(sessionmaker(bind=engine))


@pytest.fixture
def test_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


from test.factory.lot import LotFactory


@pytest.fixture
def test_lot(test_session):
    LotFactory.create(origin_price=100000, currency_pair="BTCZAR", valr_id="test-1")
