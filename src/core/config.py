import os

from dotenv import load_dotenv

load_dotenv()


api_secret: str = os.getenv("API_SECRET")
api_key: str = os.getenv("API_KEY")
root_url: str = os.getenv("ROOT_URL")
c_id: str = os.getenv("C_ID")
correction_number: int = int(os.getenv("CORRECTION_NUMBER"))
step: int = int(os.getenv("STEP"))
max_buy_lots: int = int(os.getenv("MAX_BUY_LOTS"))
max_sell_lots: int = int(os.getenv("MAX_SELL_LOTS"))
currency_pair: str = os.getenv("CURRENCY_PAIR")
# quantity: str = os.getenv("QUANTITY")
quantity: float = float(os.getenv("QUANTITY"))
post_only: bool = bool(os.getenv("POST_ONLY"))
time_in_force: str = os.getenv("TIME_IN_FORCE")
batch_lot_size: int = int(os.getenv("BATCH_LOT_SIZE"))
batch_cancel_type: str = os.getenv("BATCH_CANCEL_TYPE")
