from src.logic.lot.utils import (
    batch_lot_generation,
    filtered_open_orders,
    gen_customer_order_id,
    minimum_quantity_generation,
    post_lot_generation,
)
from src.models import ConLot


# def test_gen_customer_order_id(mocker) -> None:
#     mocker.patch("src.logic.lot.lot.c_id", new="Random")
#     r1 = gen_customer_order_id(1.0, "BTCZAR")
#     r2 = gen_customer_order_id(44535345, "kjsdkjfk")
#     assert type(r1) == str
#     assert r1 == "RandomBTCZAR1-0"
#     assert r2 == "Randomkjsdkjfk44535345"


# def test_post_lot_generation(mocker) -> None:
#     mocker.patch("src.logic.lot.lot.minimum_quantity_generation", return_value=1.0)
#     mocker.patch("src.logic.lot.lot.gen_customer_order_id", return_value="order")
#     mocker.patch("src.logic.lot.lot.currency_pair", new="USDZAR")
#     mocker.patch("src.logic.lot.lot.post_only", new=True)
#     mocker.patch("src.logic.lot.lot.time_in_force", new="GTC")
#     r1 = post_lot_generation(1.0, side=ConLot.buy)
#     mocker.patch("src.logic.lot.lot.currency_pair", new="BTCZAR")
#     r2 = post_lot_generation(1.0, side=ConLot.sell)
#     assert r1 == {
#         "side": "BUY",
#         "quantity": 1.0,
#         "price": 1.0,
#         "pair": "USDZAR",
#         "postOnly": True,
#         "customerOrderId": "order",
#         "timeInForce": "GTC",
#     }
#     assert r2 == {
#         "side": "SELL",
#         "quantity": 1.0,
#         "price": 1,
#         "pair": "BTCZAR",
#         "postOnly": True,
#         "customerOrderId": "order",
#         "timeInForce": "GTC",
#     }


def test_batch_lot_generation():
    r1 = batch_lot_generation([], order_type="something")
    assert r1 == []
    r2 = batch_lot_generation([{"data": "a"}, {"data": "b"}], order_type="something")
    assert r2 == [
        {"type": "something", "data": {"data": "a"}},
        {"type": "something", "data": {"data": "b"}},
    ]


# def test_minimum_quantity_generation(mocker) -> None:
#     mocker.patch("src.logic.lot.lot.quantity", new="0.15")
#     r1 = minimum_quantity_generation(100.45)
#     r2 = minimum_quantity_generation(1)
#     r3 = minimum_quantity_generation(90990280948.98798987987873)
#     r4 = minimum_quantity_generation(0.123456789123456789)
#     assert type(r1) == str
#     assert r1 == "0.15"
#     assert r2 == "10.02000000"
#     assert r3 == r1
#     assert r4 == "81.16200066"


def test_buy_quantity_generation(mocker) -> None:
    pass


# def test_filtered_open_orders(mocker) -> None:
#     mocker.patch("src.logic.lot.lot.get_all_open_orders", return_value=[])
#     r1 = filtered_open_orders(pair="BICUSD")
#     assert r1 == []
#     mocker.patch(
#         "src.logic.lot.lot.get_all_open_orders",
#         return_value=[
#             {
#                 "orderId": "4b8b15d0-504e-4b5f-87ee-0060eb8c0e02",
#                 "side": "buy",
#                 "remainingQuantity": "0.0000677",
#                 "price": "148000",
#                 "currencyPair": "BTCZAR",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.0000677",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR148000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "0f2ce871-334f-4950-88e6-a91b5d1f63d7",
#                 "side": "buy",
#                 "remainingQuantity": "0.00006958",
#                 "price": "144000",
#                 "currencyPair": "BTCZAR",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.00006958",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR144000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "c9e9490b-4cfa-4278-b531-f7dc98bb03e5",
#                 "side": "buy",
#                 "remainingQuantity": "0.0000668",
#                 "price": "150000",
#                 "currencyPair": "BTCZAR",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.0000668",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR150000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "0dfdad7e-a135-4d74-9ecd-deca79300ee9",
#                 "side": "buy",
#                 "remainingQuantity": "0.00006863",
#                 "price": "146000",
#                 "currencyPair": "BTCZAR",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.00006863",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR146000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "ca23eaf4-a6ef-4894-9be8-961f56d298a4",
#                 "side": "buy",
#                 "remainingQuantity": "0.00007056",
#                 "price": "142000",
#                 "currencyPair": "BTCZAR",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.00007056",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR142000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "0dfdad7e-a135-4d74-9ecd-deca79300ee9",
#                 "side": "buy",
#                 "remainingQuantity": "0.00006863",
#                 "price": "146000",
#                 "currencyPair": "btczar",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.00006863",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR146000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#             {
#                 "orderId": "0dfdad7e-a135-4d74-9ecd-deca79300ee9",
#                 "side": "buy",
#                 "remainingQuantity": "0.00006863",
#                 "price": "146000",
#                 "currencyPair": "ZARBTC",
#                 "createdAt": "2022-10-01T18:42:01.561Z",
#                 "originalQuantity": "0.00006863",
#                 "filledPercentage": "0.00",
#                 "customerOrderId": "BOT5TESTBTCZAR146000-0",
#                 "updatedAt": "2022-10-01T18:42:01.563Z",
#                 "status": "Placed",
#                 "type": "post-only limit",
#                 "timeInForce": "GTC",
#             },
#         ],
#     )
#     r2 = filtered_open_orders(pair="BTCZAR")
#     assert len(r2) == 5
