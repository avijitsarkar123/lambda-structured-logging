"""
The lambda function to demo json structured logging
"""

import datetime
import json
import os
import logging.config

import structlog


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(message)s %(lineno)d %(pathname)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'handlers': {
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        }
    },
    'loggers': {
        '': {
            'handlers': ['json'],
            'level': logging.INFO
        }
    }
})


def add_timestamp(_, __, event_dict):
    """
    A structlog processor function to add timestamp.
    :param _:
    :param __:
    :param event_dict: The structlog event_dict
    :return: event_dict
    """
    event_dict["timestamp"] = datetime.datetime.utcnow()
    return event_dict


def add_aws_request_id(_, __, event_dict):
    """
    A structlog processor function to add AWS lambda request ID.
    :param _:
    :param __:
    :param event_dict: The structlog event_dict
    :return: event_dict
    """
    event_dict["aws_request_id"] = os.environ['aws_request_id']
    return event_dict


structlog.configure(
    processors=[
        # This performs the initial filtering, so we don't
        # evaluate e.g. DEBUG when unnecessary
        structlog.stdlib.filter_by_level,

        # Adds logger=module_name (e.g __main__)
        structlog.stdlib.add_logger_name,

        # Adds level=info, debug, etc.
        structlog.stdlib.add_log_level,

        # Performs the % string interpolation as expected
        structlog.stdlib.PositionalArgumentsFormatter(),

        # Add timestamp using a method
        add_timestamp,

        # Add AWS request ID
        add_aws_request_id,

        # Include the stack when stack_info=True
        structlog.processors.StackInfoRenderer(),

        # Include the exception when exc_info=True
        # e.g log.exception() or log.warning(exc_info=True)'s behavior
        structlog.processors.format_exc_info,

        # Decodes the unicode values in any kv pairs
        structlog.processors.UnicodeDecoder(),

        # Creates the necessary args, kwargs for log()
        structlog.stdlib.render_to_log_kwargs,
    ],

    # Our "event_dict" is explicitly a dict
    # There's also structlog.threadlocal.wrap_dict(dict) in some examples
    # which keeps global context as well as thread locals
    context_class=dict,

    # Provides the logging.Logger for the underlaying log call
    logger_factory=structlog.stdlib.LoggerFactory(),

    # Provides predefined methods - log.debug(), log.info(), etc.
    wrapper_class=structlog.stdlib.BoundLogger,

    # Caching of our logger
    cache_logger_on_first_use=True,
)

LOGGER = structlog.getLogger("test")


def lambda_handler(event, context):

    """
    The lambda handler function.
    :param event: The lambda event payload
    :param context: The lambda context dict
    :return: None
    """

    os.environ['aws_request_id'] = context.aws_request_id

    LOGGER.info('## ENVIRONMENT VARIABLES')
    LOGGER.info(os.environ)
    LOGGER.info('## EVENT')
    LOGGER.info(event, key='value')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
