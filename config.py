import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    TESTNET: bool = True
    BASE_URL: str = "https://testnet.binancefuture.com"
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()

# Validate required settings
if not settings.BINANCE_API_KEY or not settings.BINANCE_API_SECRET:
    raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file") 