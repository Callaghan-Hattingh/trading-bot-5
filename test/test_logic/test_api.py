from src.logic import api
from src.models import ConTrade, ConLot
import pytest

path_generic_request = "src.logic.api.generic_request"
default_order_path = "/v1/orders/BTCZAR"


def test_get_all_open_orders(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda x, y: (x, y))
    r1 = api.get_all_open_orders()
    assert r1 == ("GET", "/v1/orders/open")


def test_get_trade_hist(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda x, y: (x, y))
    r1 = api.get_trade_hist(pair=ConTrade.bzar, skip=2, limit=10)
    assert r1 == ("GET", "/v1/marketdata/BTCZAR/tradehistory?skip=2&limit=10")


def test_get_order_history_detail(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda x, y: (x, y))
    r1 = api.get_order_history_detail(customer_id="test-1")
    r2 = api.get_order_history_detail(order_id="test-2")
    assert r1 == ("GET", "/v1/orders/history/detail/customerorderid/test-1")
    assert r2 == ("GET", "/v1/orders/history/detail/orderid/test-2")
    with pytest.raises(ValueError):
        api.get_order_history_detail()


def test_get_order_history_summary(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda x, y: (x, y))
    r1 = api.get_order_history_summary(customer_id="test-1")
    r2 = api.get_order_history_summary(order_id="test-2")
    assert r1 == ("GET", "/v1/orders/history/summary/customerorderid/test-1")
    assert r2 == ("GET", "/v1/orders/history/summary/orderid/test-2")
    with pytest.raises(ValueError):
        api.get_order_history_summary()


def test_get_order_status(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda x, y: (x, y))
    r1 = api.get_order_status(pair=ConTrade.bzar, customer_id="trade-1")
    r2 = api.get_order_status(pair=ConTrade.bzar, order_id="trade-2")
    assert r1 == ("GET", "/v1/orders/BTCZAR/customerorderid/trade-1")
    assert r2 == ("GET", "/v1/orders/BTCZAR/orderid/trade-2")
    with pytest.raises(ValueError):
        api.get_order_status(pair=ConTrade.bzar)


def test_post_limit_order(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda *args, **kwargs: (args, kwargs))
    r1 = api.post_limit_order(
        side=ConLot.buy,
        amount=0.2343,
        price=453434,
        customer_id="cid1",
        pair=ConLot.bzar,
        post_type=True,
    )
    assert r1 == (
        ("POST", "/v1/orders/limit"),
        {
            "payload": '{"side": "BUY", "quantity": 0.2343, "price": 453434, "pair": "BTCZAR", "postOnly": true, "customerOrderId": "cid1"}'
        },
    )


def test_del_order(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda *args, **kwargs: (args, kwargs))
    r1 = api.del_order(pair=ConLot.bzar, customer_id="cid1")
    r2 = api.del_order(pair=ConLot.bzar, order_id="cid1")
    assert r1 == (
        ("DELETE", "/v1/orders/order"),
        {"payload": '{"customerOrderId": "cid1", "pair": "BTCZAR"}'},
    )
    assert r2 == (
        ("DELETE", "/v1/orders/order"),
        {"payload": '{"orderId": "cid1", "pair": "BTCZAR"}'},
    )
    with pytest.raises(ValueError):
        api.del_order(pair=ConLot.bzar)


def test_batch_orders(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda *args, **kwargs: (args, kwargs))
    r1 = api.batch_orders({"a": 1, "b": 2, "c": 3})
    assert r1 == (
        ("POST", "/v1/batch/orders"),
        {"payload": '{"requests": {"a": 1, "b": 2, "c": 3}}'},
    )


def test_del_all_orders_for_pair(mocker) -> None:
    mocker.patch(path_generic_request, new=lambda *args, **kwargs: (args, kwargs))
    r1 = api.del_all_orders_for_pair(pair=ConLot.bzar)
    assert r1 == (("DELETE", default_order_path), {})


def test_generate_headers(mocker) -> None:
    mocker.patch("src.logic.api.time.time", return_value=1666205773.3395753)
    r1 = api.generate_headers("POST", default_order_path, "")
    r2 = api.generate_headers("GET", default_order_path, "{'a':1, 'b',2}")
    assert r1 == {
        "X-VALR-API-KEY": "009a2e4198c0953de7b985b8ae0bd620bc131638a857051fef1fa8214540fb23",
        "X-VALR-SIGNATURE": "3910e57e2881ee7a48c8654c443ac4d42a7c55a5cf41143c9be479dcc536c10f69b8ffc112ac6921eb63f5180bf70d88e350171387c85f753b2e7089e773e92c",
        "X-VALR-TIMESTAMP": "1666205773339",
        "Content-Type": "application/json",
    }
    assert r2 == {
        "X-VALR-API-KEY": "009a2e4198c0953de7b985b8ae0bd620bc131638a857051fef1fa8214540fb23",
        "X-VALR-SIGNATURE": "bca369b6af59ec2e6340c2da3edfedabd8ac47a0972eb65c2fc7df35e7541b730f4fe1fb8fef0e87c3fba016640768501d80f28d27ce1f036eefa5a02ebc04a1",
        "X-VALR-TIMESTAMP": "1666205773339",
        "Content-Type": "application/json",
    }


def test_generate_request(mocker) -> None:
    mocker.patch(
        "src.logic.api.requests.request", new=lambda *args, **kwargs: (args, kwargs)
    )
    r1 = api.generate_request(
        "GET", default_order_path, {"a": 1, "b": 2}, "{'c': 3, 'd': 4}"
    )
    r2 = api.generate_request("GET", default_order_path, {"a": 1, "b": 2}, "")
    assert r1 == (
        ("GET", "https://api.valr.com/v1/orders/BTCZAR"),
        {"headers": {"a": 1, "b": 2}, "data": "{'c': 3, 'd': 4}"},
    )
    assert r2 == (
        ("GET", "https://api.valr.com/v1/orders/BTCZAR"),
        {"headers": {"a": 1, "b": 2}, "data": {}},
    )


def test_generic_request(mocker) -> None:
    mocker.patch("src.logic.api.generate_headers", return_value={"e": 5, "f": 6})
    mock_generate_request = mocker.patch("src.logic.api.generate_request")
    mock_generate_request.return_value.ok = True
    mock_generate_request.return_value.json.return_value = {"a": 1}
    r1 = api.generic_request("GET", default_order_path)
    r2 = api.generic_request("GET", default_order_path, payload="")
    assert r1 == {"a": 1}
    assert r2 == {"a": 1}
    mock_generate_request.return_value.ok = False
    with pytest.raises(api.VALRapiError):
        api.generic_request("GET", default_order_path)
