from datetime import datetime
import os
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    filename='user/user.log',
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def log_user_action(user_id: str, action: str, log_level: str = "INFO"):
    log_message = f"User ID: {user_id} performed action: {action} on {datetime.now()}"

    if log_level.upper() == "ERROR":
        logging.error(log_message)
    elif log_level.upper() == "WARNING":
        logging.warning(log_message)
    else:
        logging.info(log_message)
