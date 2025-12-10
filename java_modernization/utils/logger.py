# utils/logger.py

from loguru import logger
import sys
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logger
logger.remove()  # Remove the default logger
logger.add(sys.stdout, level="INFO", colorize=True, format="<green>{time: YYYY-MM-DD > HH:mm:ss}</green> [{name}] {level} {file.name}:{line}-{message}")
logger.add("logs/code-conversion-wc.log", rotation="1 MB", retention="10 days", level="DEBUG", format="{time: YYYY-MM-DD > HH:mm:ss} {level} {message}")