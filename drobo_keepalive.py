from datetime import datetime
import logging
import os
import sys
import time

import pytz


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


def get_args_from_env():
    """Get and return runtime arguments from environment variables."""
    global logger

    logger.debug('Parsing environment variables to get drobo path.')
    try:
        drobo_path = os.environ['DROBO_PATH']
        logger.debug(f'Drobo path was specified as {drobo_path}')
    except KeyError:
        logger.debug('No drobo path was specified. Defaulting to /drobo/Videos.')
        drobo_path = '/drobo/Videos'

    logger.debug('Parsing environment variables to get sleep duration.')
    try:
        sleep_duration = int(os.environ['SLEEP_DURATION'])
    except KeyError:
        logger.debug('No sleep duration was specified. Defaulting to 60 seconds.')
        sleep_duration = 60
    except TypeError:
        logger.critical('Failed to parse sleep duration. Illegal value "{sys.argv[2]}" specified. Exiting')
        sys.exit(1)

    return (drobo_path, sleep_duration)


def keepalive(drobo_path, sleep_duration):
    """Continuously write a file on the Drobo to keep it from sleeping."""
    global logger

    try:
        now = datetime.now().replace(microsecond=0)
        pacific_time = pytz.timezone('America/Los_Angeles')
        local_time = pacific_time.localize(now).strftime('%Y-%m-%d %r')
        logger.info(f'{local_time}: Writing keepalive file to {str(drobo_path)}.')

        with open(drobo_path + '/.keepalive', 'w') as drobo_file:
            drobo_file.write(local_time + '\n')
        time.sleep(sleep_duration)
        return True

    except PermissionError:
        logger.info(f'{now}: Failed to write keepalive file on {str(drobo_path)}.')
        return False


def main():
    global logger
    drobo_path, sleep_duration = get_args_from_env()
    failed = 0

    try:
        while True:
            alive = keepalive(drobo_path, sleep_duration)

            if not alive:
                failed += 1

            if failed >= 10:
                logger.critical('Unable to write keepalive file for some reason. Exiting.')
                sys.exit(1)

    except KeyboardInterrupt:
        logger.info('CTRL+C received. Exiting.')
        sys.exit(1)


if __name__ == '__main__':
    main()
