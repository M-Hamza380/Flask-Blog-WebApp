import os
import sys
import logging
from datetime import datetime, timedelta
import threading
from logging.handlers import TimedRotatingFileHandler

# Step 1: Create logs directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Step 2: Get the current day name (e.g., Monday, Tuesday) and create a directory
current_day = datetime.now().strftime('%A')  # Get full day name (e.g., Monday)
day_dir = os.path.join(log_dir, current_day)
os.makedirs(day_dir, exist_ok=True)

# Step 3: Create a single time-stamped directory with the "latest" tag
current_time = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
timestamp_dir = os.path.join(day_dir, f"{current_time}_latest")
os.makedirs(timestamp_dir, exist_ok=True)

# Function to remove 'latest' tag after 5 minutes and create new info/error log files
def remove_latest_tag_and_create_new_logs():
    latest_tag_removed_dir = timestamp_dir.replace('_latest', '')
    os.rename(timestamp_dir, latest_tag_removed_dir)
    
    # Create new time-stamped log files after removing the latest tag
    new_timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    
    new_info_log_filepath = os.path.join(day_dir, f"info_{new_timestamp}.log")
    new_error_log_filepath = os.path.join(day_dir, f"error_{new_timestamp}.log")
    
    # Configure new log files
    new_info_handler = logging.FileHandler(new_info_log_filepath)
    new_info_handler.setLevel(logging.INFO)
    new_info_handler.setFormatter(logging.Formatter(logs_format))
    
    new_error_handler = logging.FileHandler(new_error_log_filepath)
    new_error_handler.setLevel(logging.ERROR)
    new_error_handler.setFormatter(logging.Formatter(logs_format))
    
    # Add the new handlers to the logger
    logger.addHandler(new_info_handler)
    logger.addHandler(new_error_handler)

# Start a timer to remove 'latest' tag after 5 minutes (300 seconds)
timer = threading.Timer(300, remove_latest_tag_and_create_new_logs)
timer.start()

# Step 4: Define paths for initial logs with 'latest' tag
info_log_filepath = os.path.join(timestamp_dir, 'info.log')
error_log_filepath = os.path.join(timestamp_dir, 'error.log')

# Step 5: Set up logging
logs_format = "[ [%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(message)s ]"

logger = logging.getLogger('flaskblog')
logger.setLevel(logging.INFO)

# INFO level handler
info_handler = TimedRotatingFileHandler(info_log_filepath, when="m", interval=1, backupCount=5)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(logs_format))

# ERROR level handler
error_handler = TimedRotatingFileHandler(error_log_filepath, when="m", interval=1, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(logs_format))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(logs_format))

# Add handlers to logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

