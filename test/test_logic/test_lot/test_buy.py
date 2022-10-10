import src.core.config
from src.logic.lot.buy import (
    create_planned_lots,
    open_buy_lots,
    lots_to_place,
    lots_placed_to_be_cancelled,
    check_to_place,
    pre_buy_db_add,
    batch_post_buy_lots,
    buy_controller,
)
from test.data import d1
from src.models import Lot
from unittest.mock import patch


def test_create_planned_lots(mocker) -> None:
    mocker.patch("src.logic.lot.buy.step", new=1000)
    mocker.patch("src.logic.lot.buy.max_buy_lots", new=2)
    r1 = create_planned_lots(23453.48)
    assert len(r1) == 2
    assert r1 == {22000.0, 21000.0}


def test_open_buy_lots() -> None:
    r1 = open_buy_lots(d1)
    assert len(r1) == 5
    assert r1 == {148000.0, 144000.0, 142000.0, 150000.0, 146000.0}


def test_lots_to_place() -> None:
    r1 = lots_to_place(
        placed_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
        planned_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
    )
    assert r1 == set()
    r2 = lots_to_place(
        placed_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
        planned_lots={148000.0, 146000.0},
    )
    assert r2 == set()
    r3 = lots_to_place(
        placed_lots={148000.0, 146000.0},
        planned_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
    )
    assert r3 == {144000.0, 150000.0, 142000.0}


def test_lots_placed_to_be_cancelled() -> None:
    r1 = lots_placed_to_be_cancelled(
        placed_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
        planned_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
    )
    assert r1 == set()
    r2 = lots_placed_to_be_cancelled(
        placed_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
        planned_lots={148000.0, 146000.0},
    )
    assert r2 == {144000.0, 142000.0}
    r3 = lots_placed_to_be_cancelled(
        placed_lots={148000.0, 146000.0},
        planned_lots={148000.0, 144000.0, 142000.0, 150000.0, 146000.0},
    )
    assert r3 == set()


def test_check_to_place_blank_db(test_session, mocker) -> None:
    mocker.patch("src.logic.lot.lot.c_id", new="")
    mocker.patch("src.logic.lot.buy.get_origin_price", return_value=[])
    # mocker.patch("src.logic.lot.buy.get_origin_price", return_value=Lot())
    mocker.patch("src.logic.lot.buy.pre_buy_db_add", return_value=None)
    r1 = check_to_place({148000.0})
    assert r1 == [
        {
            "side": "BUY",
            "quantity": "0.00006770",
            "price": 148000,
            "pair": "BTCZAR",
            "postOnly": True,
            "customerOrderId": "BTCZAR148000",
            "timeInForce": "GTC",
        }
    ]
