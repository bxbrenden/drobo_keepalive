from datetime import datetime
import sys


def keepalive(drobo_path):
    """Continuously write a file on the Drobo to keep it from sleeping."""
    try:
        now = str(datetime.now().replace(microsecond=0))
        with open(drobo_path + '/.keepalive', 'w') as drobo_file:
            print(f'{now}: Writing keepalive file to {str(drobo_path)}.')
            drobo_file.write(now)
        return True
    except PermissionError:
        print(f'{now}: Failed to write keepalive file on {str(drobo_path)}.')
        return False


def main():
    while True:
        failed = 0
        alive = keepalive('/drobo/Videos')

        if not alive:
            failed += 1

        if failed > 10:
            print('Unable to write keepalive file for some reason. Exiting.')
            sys.exit(1)


if __name__ == '__main__':
    main()
