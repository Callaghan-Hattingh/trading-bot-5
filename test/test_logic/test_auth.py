from src.logic.auth import Auth, api_key


def test_sign_request() -> None:
    r = Auth.sign_request(1652958074138, "GET", "/v1/orders/open")
    assert (
            r
            == "037220009189eda4fdd1a43fcc96f9bf642e1a93803de25746f3d1e73e37b908"
               "6513c07bcc94b99a2d570f1868cde670310160f48eda20b1b8cd75b6361150f8"
    )


def test_get_headers() -> None:
    r = Auth.get_headers(
        1652958074138,
        "037220009189eda4fdd1a43fcc96f9bf642e1a93803de25746f3d1e73e37b908",
    )
    assert r == {
        "X-VALR-API-KEY": f"{api_key}",
        "X-VALR-SIGNATURE": "037220009189eda4fdd1a43fcc96f9bf642e1a93803de25746f3d1e73e37b908",
        "X-VALR-TIMESTAMP": "1652958074138",
        "Content-Type": "application/json",
    }
