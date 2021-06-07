from datetime import datetime
import logging
import sys
import time


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('/app/logs/keepalive.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


logger = configure_logging()


def keepalive(drobo_path, sleep_duration):
    """Continuously write a file on the Drobo to keep it from sleeping."""
    global logger

    try:
        now = str(datetime.now().replace(microsecond=0))
        logger.info(f'{now}: Writing keepalive file to {str(drobo_path)}.')

        with open(drobo_path + '/.keepalive', 'w') as drobo_file:
            drobo_file.write(now)
        time.sleep(sleep_duration)
        return True

    except PermissionError:
        logger.info(f'{now}: Failed to write keepalive file on {str(drobo_path)}.')
        return False


def main():
    global logger
    drobo_path = '/drobo/Videos'
    sleep_duration = 10
    failed = 0

    try:
        while True:
            alive = keepalive(drobo_path, sleep_duration)

            if not alive:
                failed += 1

            if failed >= 10:
                logger.info('Unable to write keepalive file for some reason. Exiting.')
                sys.exit(1)

    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()
