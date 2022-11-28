from src.logic.lot.buy.buy_to_cancel import (
    list_of_planned_buy_act_to_buy_pass_lots,
    list_of_planned_buy_act_lots,
)


def test_list_of_planned_buy_act_lots(mocker) -> None:
    mocker.patch("src.logic.lot.buy.buy_to_cancel.step", new=1000)
    mocker.patch("src.logic.lot.buy.buy_to_cancel.max_buy_lots", new=5)
    r1 = list_of_planned_buy_act_lots(price=100000)
    assert r1 == {96000, 97000, 98000, 95000, 99000}


def test_list_of_planned_buy_act_to_buy_pass_lots(mocker) -> None:
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
