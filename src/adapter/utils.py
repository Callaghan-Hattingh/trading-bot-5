from src.db.base import session


def commit() -> None:
    session.commit()
