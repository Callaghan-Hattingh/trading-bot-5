from src.logic.lot.buy.buy_to_cancel import (
    list_of_planned_buy_act_to_buy_pass_lots,
    list_of_planned_buy_act_lots,
    create_cancel_lots_batch_buy_act_to_buy_pass,
)


def test_list_of_planned_buy_act_lots(mocker) -> None:
    mocker.patch("src.logic.lot.buy.buy_to_cancel.step", new=1000)
    mocker.patch("src.logic.lot.buy.buy_to_cancel.max_buy_lots", new=5)
    r1 = list_of_planned_buy_act_lots(price=100000)
    assert r1 == {96000, 97000, 98000, 95000, 99000}


def test_list_of_planned_buy_act_to_buy_pass_lots() -> None:
    r1 = list_of_planned_buy_act_to_buy_pass_lots(
        placed_buy_act={96000, 97000, 98000, 95000, 99000},
        planned_buy_act={96000, 97000, 98000, 95000, 99000},
    )
    assert r1 == set()
    r2 = list_of_planned_buy_act_to_buy_pass_lots(
        placed_buy_act={96000, 97000, 98000, 95000, 99000},
        planned_buy_act={96000, 97000, 98000, 100000, 99000},
    )
    assert r2 == {95000}
    r3 = list_of_planned_buy_act_to_buy_pass_lots(
        placed_buy_act={96000, 97000, 98000, 95000, 99000},
        planned_buy_act={97000},
    )
    assert r3 == {96000, 95000, 99000, 98000}


def test_create_cancel_lots_batch_buy_act_to_buy_pass(
    mocker, test_session, test_types_lots
) -> None:
    mocker.patch(
        "src.logic.lot.buy.buy_to_cancel.read_lot_id_of_buy_act", return_value="uuid"
    )
    r1 = create_cancel_lots_batch_buy_act_to_buy_pass(
        buy_act_lots_to_cancel={100000, 99000}
    )
    assert r1 == [
        {"type": "CANCEL_ORDER", "data": {"orderId": "uuid", "pair": "BTCZAR"}},
        {"type": "CANCEL_ORDER", "data": {"orderId": "uuid", "pair": "BTCZAR"}},
    ]
