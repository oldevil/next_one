import logging

from functools import wraps

logger = logging.getLogger('deco')


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        detail = {
            'FUNCTION_NAME': func.__name__,
            'REMOTE_ADDR': args[0].META.get('REMOTE_ADDR', 'unknown'),
            'HTTP_USER_AGENT': args[0].META.get('HTTP_USER_AGENT', 'unknown'),
        }
        logger.info(detail)
        return func(*args, **kwargs)
    return with_logging
