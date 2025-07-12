import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%D_%Y_%H_%M_%S')}.log"

""" 
 :: OLD CODE ::
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) """

# Create logs directory path
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create full path to log file
logs_path = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(
    filename=logs_path,
    format="[%(asctime)s ]%(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

""" Code to test logging setup
if __name__ == "__main__":
    logging.info("Logging setup complete.")
    print(f"Logs will be saved to {logs_path}")"""