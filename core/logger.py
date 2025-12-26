import time
import logging
import logging.handlers
from .config import logs_dir

def setup_logger(name='prawl', level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    log_dir = logs_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    # max 10mb, up to 5 files archive
    log_file = log_dir / f'prawl_{time.strftime("%Y-%m-%d")}.log'
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5, encoding='utf-8')
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d | %(message)s'))
    logger.addHandler(fh)

    # console
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
    ))
    logger.addHandler(ch)

    logger.info('-------------------------------------------')
    logger.info('logger started')
    return logger

def log_ee(func):
    """decorator for auto entry/exit and exception logging"""
    logger = logging.getLogger('prawl')
    def wrapper(*args, **kwargs):
        logger.debug(f'→ {func.__module__}.{func.__qualname__}')
        try:
            result = func(*args, **kwargs)
            logger.debug(f'← {func.__module__}.{func.__qualname__}')
            return result
        except Exception as e:
            logger.exception(f'✗ exception in {func.__module__}.{func.__qualname__}: {e}')
            raise
    return wrapper
