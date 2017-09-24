"""Settings module."""

from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv


def basepath(*args):
    """Joints path since basepath."""
    return join(dirname(__file__), '../../', *args)


def load_environment(env='develop'):
    """Load env.{scope} file."""
    load_dotenv(basepath('config', 'env.{}'.format(
        environ.get('APP_ENV', env)
    )))


load_environment()


SETTINGS = {
    'mongo': {
        'uri': environ.get('MONGO_URI'),
        'db': environ.get('MONGO_DB'),
    }
}
