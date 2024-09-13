import os
import logging.config
from pythonjsonlogger import jsonlogger
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from dotenv import load_dotenv

load_dotenv()

log_level = os.environ.get('LOG_LEVEL', 'ERROR')
sentry_dsn = os.environ.get('SENTRY_DSN')

# Step 1: Initialize Sentry SDK with Logging Integration
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

if sentry_dsn:
    # Initialize Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[sentry_logging],
        traces_sample_rate=0.5,
        profiles_sample_rate=0.5,
    )

# Step 2: Define your logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout"],
            "level": log_level,
            "propagate": True
        }
    },
}

if sentry_dsn:
    LOGGING["handlers"]["sentry"] = {
        "level": "ERROR",
        "class": "sentry_sdk.integrations.logging.EventHandler",
    }
    LOGGING["loggers"][""]["handlers"].append("sentry")
else:
    LOGGING["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": "app.log",
        "formatter": "json",
        "level": "ERROR",
    }
    LOGGING["loggers"][""]["handlers"].append("file")

# Step 3: Apply logging configuration
logging.config.dictConfig(LOGGING)

# Example usage of the logger
logger = logging.getLogger(__name__)

# Demo
# logger.error("This is an error log message.")
