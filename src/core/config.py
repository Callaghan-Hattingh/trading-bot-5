import os

from dotenv import load_dotenv

load_dotenv()


api_secret: str = os.getenv("API_SECRET")
api_key: str = os.getenv("API_KEY")
root_url: str = os.getenv("ROOT_URL")
c_id: str = os.getenv("C_ID")
correction_number: int = int(os.getenv("CORRECTION_NUMBER"))
step: int = int(os.getenv("STEP"))
max_buy_orders: int = int(os.getenv("MAX_BUY_ORDERS"))
max_sell_orders: int = int(os.getenv("MAX_SELL_ORDERS"))
currency_pair: str = os.getenv("CURRENCY_PAIR")
quantity: float = float(os.getenv("QUANTITY"))
post_only: bool = bool(os.getenv("POST_ONLY"))
time_in_force: str = os.getenv("TIME_IN_FORCE")

