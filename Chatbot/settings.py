from dotenv import load_dotenv
import os

load_dotenv()  # بارگذاری فایل .env

DB_URL = os.getenv("DB_URL", "sqlite:///chat.db")
EDEN_PROVIDER = os.getenv("EDEN_PROVIDER", "openai")
EDEN_MODEL = os.getenv("EDEN_MODEL", "gpt-3.5-turbo")
EDENAI_API_KEY = os.getenv("EDENAI_API_KEY")
COOKIE_PASSWORD = os.getenv("COOKIE_PASSWORD")