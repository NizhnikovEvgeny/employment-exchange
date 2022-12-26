from starlette.config import Config
import os

DATABASE_URL = "postgresql://postgres:postgres@localhost:32700/employment_exchange"

config = Config(".env_dev")
ACCESS_TOKEN_EXPIRE_MINUTES = 600000
ENCODE_ALGORITHM = "HS256"
SECRET_KEY = config("EE_SECRET_KEY", cast=str, default="")
# DATABASE_URL = config("EE_DATABASE_URL", cast=str, default="")
# else:
if os.environ.get('DB_HOST') is not None:
    DATABASE_HOST = os.environ.get('DB_HOST')
    DATABASE_NAME = os.environ.get('DB_NAME')
    DATABASE_USERNAME = os.environ.get('DB_USER')
    DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
    DATABASE_PORT = os.environ.get('DB_PORT')
    DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
