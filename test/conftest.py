import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
def test_default_lot(test_session):
    LotFactory.create(origin_price=100000, currency_pair="BTCZAR", valr_id="test-1")


@pytest.fixture
def test_types_lots(test_session):
    for i in range(97000, 100000, 1000):
        LotFactory.create(
            origin_price=i,
            currency_pair="BTCZAR",
            valr_id="test-2",
            order_status="buy_passive",
        )

    for i in range(100000, 103000, 1000):
        LotFactory.create(
            origin_price=i,
            price=i * 1.01,
            currency_pair="BTCZAR",
            valr_id="test-2",
            order_status="buy_active",
        )

    for i in range(107000, 120000, 1000):
        LotFactory.create(
            origin_price=i,
            price=i * 1.01,
            currency_pair="BTCZAR",
            valr_id="test-2",
            order_status="sell_active",
        )

    for i in range(120000, 123000, 1000):
        LotFactory.create(
            origin_price=i,
            currency_pair="BTCZAR",
            valr_id="test-2",
            order_status="sell_passive",
        )
