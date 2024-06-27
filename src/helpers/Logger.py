from pythonjsonlogger import jsonlogger
import logging.config

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        if record.stack_info:
            record.exc_info = record.stack_info
        else:
            record.stack_info = ''
        return super(CustomJsonFormatter, self).format(record)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed_json": {
            "()": CustomJsonFormatter,
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s . %(stack_info)s"
        },
        "standard": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s ."
        }
    },
    "handlers": {
        "json_file": {
            "class": "logging.FileHandler",
            "filename": "../logs/xmlc-watcher.log",
            "formatter": "detailed_json"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "xmlc-watcher": {
            "handlers": ["json_file", "console"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}