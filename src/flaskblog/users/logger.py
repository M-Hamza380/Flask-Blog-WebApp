import os, sys, logging

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filepath = os.path.join(log_dir, 'running_log.log')

logs_format = "[ [%(asctime)s] : %(name)s : %(levelname)s : %(module)s : %(message)s ]"

logging.basicConfig(
    level=logging.INFO,
    format=logs_format,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('flaskblog')

