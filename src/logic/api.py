import json
import time

import requests

from src.core.config import root_url
# from src.core.logcon import logger
from src.logic.auth import Auth


class VALRapiError(Exception):
    pass


def generic_request(verb: str, path: str, *, payload: str = None) -> dict:
    timestamp = int(time.time() * 1000)
    if payload:
        signature = Auth.sign_request(timestamp, verb, path, body=payload)
    else:
        signature = Auth.sign_request(timestamp, verb, path)

    url = f"{root_url}{path}"
    if payload is None:
        payload = {}

    headers = Auth.get_headers(timestamp, signature)

    response = requests.request(verb, url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        # logger.error("%s: %s", path, response.json())
        raise VALRapiError(response.json())


class ValrApi:
    @staticmethod
    def get_all_open_orders() -> dict:
        verb = "GET"
        path = "/v1/orders/open"
        return generic_request(verb, path)

    @staticmethod
    def get_trade_hist(*, pair: str, skip: int, limit: int) -> dict:
        verb = "GET"
        path = f"/v1/marketdata/{pair}/tradehistory?skip={skip}&limit={limit}"
        return generic_request(verb, path)

    @staticmethod
    def get_order_history_detail(*, customer_id: str = None, order_id: str = None):
        # get the lot history detail of the last successfully placed lot
        if customer_id is not None:
            path = f"/v1/orders/history/detail/customerorderid/{customer_id}"
        elif order_id is not None:
            path = f"/v1/orders/history/detail/orderid/{order_id}"
        else:
            raise ValueError("Must provide either customer_id or order_id")
        verb = "GET"
        return generic_request(verb, path)

    @staticmethod
    def get_order_history_summary(*, customer_id: str = None, order_id: str = None):
        # get the lot history summary of the last successfully placed lot
        if customer_id is not None:
            path = f"/v1/orders/history/summary/customerorderid/{customer_id}"
        elif order_id is not None:
            path = f"/v1/orders/history/summary/orderid/{order_id}"
        else:
            raise ValueError("Must provide either customer_id or order_id")
        verb = "GET"
        return generic_request(verb, path)

    @staticmethod
    def get_order_status(
        *, pair: str = "BTCZAR", customer_id: str = None, order_id: str = None
    ):
        # call only directly after placing lot
        if customer_id is not None:
            path = f"/v1/orders/{pair}/customerorderid/{customer_id}"
        elif order_id is not None:
            path = f"/v1/orders/{pair}/orderid/{order_id}"
        else:
            raise ValueError("Must provide either customer_id or order_id")
        verb = "GET"
        return generic_request(verb, path)

    @staticmethod
    def post_limit_order(
        side: str,
        amount: float,
        price: int,
        customer_id: str = None,
        *,
        pair: str = "BTCZAR",
        post_type: bool = True,
    ):
        verb = "POST"
        path = "/v1/orders/limit"
        payload = json.dumps(
            {
                "side": side,
                "quantity": amount,
                "price": price,
                "pair": pair,
                "postOnly": post_type,
                "customerOrderId": customer_id,
            }
        )
        return generic_request(verb, path, payload=payload)

    @staticmethod
    def del_order(
        *, pair: str = "BTCZAR", customer_id: str = None, order_id: str = None
    ):
        verb = "DELETE"
        path = "/v1/orders/order"

        if customer_id is not None:
            payload = json.dumps({"customerOrderId": customer_id, "pair": pair})
        elif order_id is not None:
            payload = json.dumps({"orderId": order_id, "pair": pair})
        else:
            raise ValueError("Must provide either customer_id or order_id")
        return generic_request(verb, path, payload=payload)

    @staticmethod
    def batch_orders(data):
        verb = "POST"
        path = "/v1/batch/orders"
        payload = json.dumps({"requests": data})
        print(payload)
        return generic_request(verb, path, payload=payload)

    @staticmethod
    def del_all_orders_for_pair(*, pair: str = "BTCZAR"):
        verb = "DELETE"
        path = f"/v1/orders/{pair}"
        return generic_request(verb, path)
