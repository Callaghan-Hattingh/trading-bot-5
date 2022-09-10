from src.models import Order, OrderFactory


def test_order(session):
    q = session.query(Order).all()
    assert q == []
    OrderFactory.create()
    q = session.query(Order).all()
    assert q != []
