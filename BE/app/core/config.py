import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    database_url: str = os.getenv("DATABASE_URL")
    cors_origins: str = os.getenv("CORS_ORIGINS")
    default_pw: str = os.getenv("DEFAULT_PW")

settings = Settings()