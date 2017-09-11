
[![Build Status](https://travis-ci.org/sonic182/aiohttp_sample.svg?branch=master)](https://travis-ci.org/sonic182/aiohttp_sample)
[![Coverage Status](https://coveralls.io/repos/github/sonic182/aiohttp_sample/badge.svg?branch=master)](https://coveralls.io/github/sonic182/aiohttp_sample?branch=master)
# AIOTEST

Sample framework for aiohttp.

# Development

Install packages with pip-tools:
```bash
pip install pip-tools
pip-compile
pip-compile dev-requirements.in
pip-sync requirements.txt dev-requirements.txt
```

# TODO

* cookiecutter based on this sample project
* JSON input validation with schemes
* Maybe better logger
* Middlewares sample (append info to request, eg: logged user)
* Better tests

# Contribute

1. Fork
2. create a branch `feature/your_feature`
3. commit - push - pull request

Thanks :)
