#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : logger.py
# @Author: Wanglei
# @Date  : 2018/4/29
# @Desc  :

import logging.config
# Log config
LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stderr'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': 'log/info.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'encoding': 'utf8'
        },
        'debug_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'log/debug.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'default',
            'filename': 'log/error.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'proxy': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'crawl': {
            'handlers': ['debug_file_handler', 'error_file_handler'],
            'level': 'DEBUG'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'debug_file_handler']
    }
}


logging.config.dictConfig(LOGCONFIG)
logger = logging.getLogger()



