"""Main script."""
import argparse

from aiohttp import web

from app.config.logger import LOGGER
from app.config.application import app_config


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

    parser.add_argument(
        '--debug',
        action='store_true',
    )

    args = parser.parse_args()

    app = web.Application(debug=args.debug, logger=LOGGER)
    app_config(app)
    app.logger.info('starting_app', extra={'port': args.port})
    web.run_app(app, port=args.port)


if __name__ == '__main__':
    main()
