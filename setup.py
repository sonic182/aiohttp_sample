"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
# from setuptools import find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
REQS = [str(ir.req) for ir in parse_requirements('requirements.txt',
                                                 session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements('dev-requirements.txt',
                                                  session='hack')]
# HERE = path.abspath(path.dirname(__file__))
# Get the long description from the README file
# with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name='aiohttp_bootstrap',
    version='0.0.1',
    description='Bootstrap project for aiohttp',
    # long_description=long_description,
    # The project's main homepage.
    # url='https://github.com/pypa/sampleproject',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=REQS,
    extra_requires={
        'test': REQS2
    }
)
