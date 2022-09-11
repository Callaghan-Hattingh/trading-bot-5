import os

from dotenv import load_dotenv

load_dotenv()


api_secret: str = os.getenv("API_SECRET")
api_key: str = os.getenv("API_KEY")
root_url: str = os.getenv("ROOT_URL")
