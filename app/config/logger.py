
import logging
import collections

from app.config.settings import basepath

LOGGER = logging.getLogger('aiohttp_sample')
LOGGER.setLevel(logging.DEBUG)

FH = logging.FileHandler(basepath('logs', 'my.log'))
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('%(asctime)s; LEVEL=%(levelname)s; %(message)s')

FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


class myLogger(logging.LoggerAdapter):
    def process(self, msg, extra={}, **kwargs):
        """Proccess stupid message."""
        if isinstance(extra['extra'], dict):
            extra = extra['extra']

        extra = {
            **extra,
            'type': msg,
        }
        extra = collections.OrderedDict(sorted(extra.items()))

        def _print_extras(extra, key=''):
            res = ''
            if isinstance(extra, dict):
                for _key in extra:
                    temp_key = '{}{}{}'.format(key, ('.' if key else ''), _key)
                    res += _print_extras(extra[_key], temp_key)

            elif isinstance(extra, list):
                for ind, item in enumerate(extra):
                    temp_key = '{}{}{}'.format(key, ('.' if key else ''), ind)
                    res += _print_extras(item, temp_key)
            else:
                return res + '{}={}; '.format(key, extra)
            return res

        return _print_extras(extra), kwargs


LOGGER = myLogger(LOGGER, {})
