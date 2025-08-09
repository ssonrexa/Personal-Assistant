import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_NAME = "claude-3-5-sonnet-20241022"
    
    @classmethod
    def validate(cls):
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

settings = Settings()