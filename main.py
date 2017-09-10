"""Main script."""
import argparse

from aiohttp import web
from app.config.application import APP


def main():
    """Start app."""
    parser = argparse.ArgumentParser(description='Run application.')

    parser.add_argument(
        'port',
        type=int,
        default=8080,
        nargs='*',
        help='application port.'
    )

    args = parser.parse_args()
    web.run_app(APP, port=args.port)


if __name__ == '__main__':
    main()
