"""Main script."""
from os import environ

import argparse
import asyncio
import uvloop
from aiohttp import web

from app.config.settings import basepath
from app.config.logger import get_logger
from app.config.application import app_config
from app.middlewares import MIDDLEWARES

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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

    logger = get_logger(
        debug=args.debug,
        info_log=basepath('logs', 'info.log'),
        error_log=basepath('logs', 'error.log'),
    )

    app = web.Application(
        debug=args.debug,
        logger=logger,
        middlewares=MIDDLEWARES
    )
    app_config(app)
    app.logger.info('starting_app', extra={
        'port': args.port,
        'env': environ.get('APP_ENV', 'develop')
    })
    web.run_app(
        app,
        port=args.port,
        access_log=None
    )


if __name__ == '__main__':
    main()
