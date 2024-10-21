import logging
from datetime import datetime

logging.basicConfig(
    filename ='user/user.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
)


def log_user_action(user_id: str, action: str):
    log_message = f"User ID: {user_id} performed action: {action} on {datetime.now()}"
    logging.info(log_message)
