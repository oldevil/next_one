import logging

from functools import wraps

logger = logging.getLogger('deco')


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logger.info(func.__name__)
        logger.info(args[0].META['REMOTE_ADDR'])
        logger.info(args[0].META['HTTP_USER_AGENT'])
        return func(*args, **kwargs)
    return with_logging
