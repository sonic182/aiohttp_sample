#!/bin/bash

case $1 in
	"sync")
	pip install pip-tools
	pip-compile
	pip-compile dev-requirements.in
	pip-sync dev-requirements.txt requirements.txt
	;;
esac
