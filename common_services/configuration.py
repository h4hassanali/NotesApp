import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get_env_variable(var_name):
        value = os.getenv(var_name)
        if value is None:
            raise EnvironmentError(
                f"Missing required environment variable: {var_name}")
        return value
