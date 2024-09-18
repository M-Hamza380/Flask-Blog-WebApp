import logging
import os
import sys
from datetime import datetime

# Step 1: Create logs directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Step 2: Get the current day name (e.g., Monday, Tuesday) and create a directory
current_date = datetime.now().strftime("%d_%m_%Y")
date_dir = os.path.join(log_dir, current_date)
os.makedirs(date_dir, exist_ok=True)

# Step 3: Get the current day name (e.g., Monday, Tuesday) and create a directory
current_day = datetime.now().strftime("%A")
day_dir = os.path.join(date_dir, current_day)
os.makedirs(day_dir, exist_ok=True)


# Function to create a directory with the given consistent timestamp
def create_directory_with_timestamp(base_time):
    timestamp = base_time.strftime("%d_%m_%Y_%H_%M")  # Generate the timestamp once
    timestamp_dir = os.path.join(day_dir, f"Latest_{timestamp}")
    os.makedirs(timestamp_dir, exist_ok=True)
    return timestamp_dir


# Step 4: Generate base timestamp and directory
base_time = datetime.now()
timestamp_dir = create_directory_with_timestamp(base_time)

# Step 5: Define paths for both logs in the same directory
info_log_filepath = os.path.join(timestamp_dir, "info.log")
error_log_filepath = os.path.join(timestamp_dir, "error.log")

# Step 6: Set up logging format
logs_format = "[ [%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(message)s ]"

# Step 7: Set up logger and prevent duplicate handlers
logger = logging.getLogger("flaskblog")
logger.setLevel(logging.INFO)

if not logger.handlers:  # Prevent adding multiple handlers
    # INFO level handler
    info_handler = logging.FileHandler(info_log_filepath)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(logs_format))

    # ERROR level handler
    error_handler = logging.FileHandler(error_log_filepath)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(logs_format))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(logs_format))

    # Add handlers to logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
