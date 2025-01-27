import logging
from functools import wraps


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='error.log',
                    encoding='utf-8',
                    )

def error_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in function '{func.__name__}': {e}", exc_info=True,)
            raise
    return wrapper

