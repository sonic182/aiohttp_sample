"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements('requirements.txt',
                                                 session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements('dev-requirements.txt',
                                                  session='hack')]


setup(
    name='aiohttp_sample',
    version='0.0.1',
    description='Bootstrap project for aiohttp',
    url='https://github.com/sonic182/aiohttp_sample',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=REQS,
    extras_require={
        'test': REQS2
    }
)
