import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

CLIENT = os.getenv("CLIENT")

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRATION")
REFRESH_TOKEN_EXPIRATION = os.getenv("REFRESH_TOKEN_EXPIRATION")
ALGORITHM = os.getenv("ALGORITHM")
API_KEY = os.getenv("API_KEY")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

DB_CONNECTION = os.getenv("DB_CONNECTION")
UPLOAD_DIR = os.getenv("UPLOAD_DIR")