"""Main script."""
import argparse

from aiohttp import web

from app.config.logger import get_logger
from app.config.application import app_config
from app.middlewares import MIDDLEWARES


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

    app = web.Application(
        debug=args.debug,
        logger=get_logger(debug=args.debug),
        middlewares=MIDDLEWARES
    )
    app_config(app)
    app.logger.info('starting_app', extra={'port': args.port})
    web.run_app(app, port=args.port, access_log=None)


if __name__ == '__main__':
    main()
