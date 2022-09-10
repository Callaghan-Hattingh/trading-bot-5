import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.db.base import Base

engine = create_engine("sqlite:///test_sqlite.db", echo=False)
TestingSessionLocal = scoped_session(sessionmaker(bind=engine))


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
