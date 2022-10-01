from time import sleep

from .db.base import create_tables
from .logic import last_amount_traded
from .logic.api import ValrApi
from .logic.lot.buy import buy_controller
from .logic.lot.lot import filtered_open_orders


def app():
    create_tables()
    t = last_amount_traded()
    foo = filtered_open_orders()
    # t, foo = 500000, set()
    buy_controller(t, foo)
    sleep(10)
    foo = filtered_open_orders()
    print(foo)
    # buy_controller(t + 4000, foo)
    sleep(10)
    r = ValrApi.del_all_orders_for_pair()
    print(r)
