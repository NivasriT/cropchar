import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

    @classmethod
    def validate(cls):
        missing = [n for n in ("FIRMS_MAP_KEY", "EMAIL_ADDRESS", "EMAIL_APP_PASSWORD")
                   if not getattr(cls, n)]
        if missing:
            raise RuntimeError(f"Missing env vars: {', '.join(missing)}. Check your .env file.")

settings = Settings()