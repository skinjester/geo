LOGGING_CONFIG = {
    'version': 1, # required
    'disable_existing_loggers': True, # required
    'formatters': {
        'standard': {
            'format': '%(relativeCreated)010.2f [%(funcName)-s] %(message)s'
        },
        'showthread': {
            'format': '%(relativeCreated)010.2f %(threadName)-s [%(funcName)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'console-thread': {
            'class': 'logging.StreamHandler',
            'formatter': 'showthread'
        }
    },
    'loggers': {
        'mainlog': {
            'handlers': ['console'],
        },
        'threadlog': {
            'handlers': ['console-thread'],
        }
    }
}

'''
\t%(funcName)s\t%(threadName)s\t%(processName)s\t%(filename)s:%(lineno)s\t%(message)s
'''
