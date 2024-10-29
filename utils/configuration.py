import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    filename='user/user.log',
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class Config:
    @staticmethod
    def get_env_variable(var_name):
        value = os.getenv(var_name)
        if value is None:
            raise EnvironmentError(
                f"Missing required environment variable: {var_name}")
        return value
