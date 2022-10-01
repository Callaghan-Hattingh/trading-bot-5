from src.logic.trade import last_amount_traded


def test_last_amount_traded(test_session, mocker):
    mocker.patch("src.logic.trade.correction_number", new=0)
    mocker.patch(
        "src.logic.trade.ValrApi.get_trade_hist",
        return_value=[
            {
                "price": "354262",
                "quantity": "0.09002596",
                "currencyPair": "BTCZAR",
                "tradedAt": "2022-10-01T14:02:32.638Z",
                "takerSide": "sell",
                "sequenceId": 1025769692792360960,
                "id": "997aa9b3-bdeb-40f2-ad5f-c78b8a2b2608",
                "quoteVolume": "31892.77664152",
            }
        ],
    )
    t = last_amount_traded()
    assert t == 354262.0
