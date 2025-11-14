import logging

from config import LOG_DIR, LOG_LEVEL


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {'()': 'internal.core.logs.formatters.JSONFormatter'},
        'console': {'()': 'internal.core.logs.formatters.ConsoleFormatter'},
    },
    'filters': {
        'apscheduler_filter': {
            '()': 'internal.core.logs.filters.ApSchedulerFilter'
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'console',
            'class': 'logging.StreamHandler',
            'filters': ['apscheduler_filter']
        },
        'file_handler': {
            'formatter': 'json',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'{LOG_DIR}/logs.json',
            'when': 'midnight',
            'backupCount': 0,
            'filters': ['apscheduler_filter']
        },
        'null': {
            'class': 'logging.NullHandler'
        },
    },
    'loggers': {
        'root': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['file_handler'],
            'level': logging.INFO,
            'propagate': True,
        },
        'error': {
            'handlers': ['file_handler'],
            'level': logging.ERROR,
            'propagate': True,
        },
        'uvicorn': {'propagate': True},
        'uvicorn.error': {
            'handlers': [],
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': [],
            'level': logging.INFO,
            'propagate': False,
        },
        'apscheduler': {
            'level': logging.INFO,
            'handlers': ['file_handler'],
            'propagate': True,
        },
        'httpx': {
            'level': logging.ERROR,
            'handlers': ['file_handler'],
            'propagate': True,
        },
    },
}
