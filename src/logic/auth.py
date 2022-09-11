import hashlib
import hmac
import os

from src.core.config import api_secret, api_key
from src.core.logcon import logger


class Auth:
    @staticmethod
    def sign_request(
        timestamp: int,
        verb: str,
        path: str,
        *,
        api_key_secret: str = api_secret,
        body: str = "",
    ) -> str:
        """Signs the request payload using the api key secret
        api - the api key secret
        t - the unix t of this request e.g. int(time.time()*1000)
        v - Http v - GET, POST, PUT or DELETE
        p - p excluding host name, e.g. '/v1/withdraw
        body - http request body as a string, optional
        """
        payload = "{}{}{}{}".format(timestamp, verb.upper(), path, body)
        logger.debug("payload: %s", payload)
        message = bytearray(payload, "utf-8")
        signature = hmac.new(
            bytearray(api_key_secret, "utf-8"), message, digestmod=hashlib.sha512
        ).hexdigest()
        return signature

    @staticmethod
    def get_headers(timestamp: int, signature: str) -> dict:
        logger.debug("header: time:%s, sign:%s", timestamp, signature)
        header = {
            "X-VALR-API-KEY": f"{api_key}",
            "X-VALR-SIGNATURE": f"{signature}",
            "X-VALR-TIMESTAMP": f"{timestamp}",
            "Content-Type": "application/json",
        }
        return header
