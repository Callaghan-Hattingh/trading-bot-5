from .db.base import create_tables
from .logic import last_amount_traded
from .logic.lot.buy import buy_controller


def app():
    create_tables()
    # r = last_amount_traded()
    # print(r)
    buy_controller(369887)
