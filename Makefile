# Makefile for Dirus.
#
# Source:: https://github.com/ampledata/dirus
# Author:: Greg Albrecht W2GMD <oss@undef.net>
# Copyright:: Copyright 2016 Orion Labs, Inc.
# License:: Apache License, Version 2.0
#


.DEFAULT_GOAL := all


all: develop

develop: remember
	python setup.py develop

install_requirements:
	pip install -r requirements.txt

install: remember
	python setup.py install

uninstall:
	pip uninstall -y dirus

reinstall: uninstall install

remember:
	@echo
	@echo "Hello from the Makefile..."
	@echo "Don't forget to run: 'make install_requirements'"
	@echo

clean:
	@rm -rf *.egg* build dist *.py[oc] */*.py[co] cover doctest_pypi.cfg \
		nosetests.xml pylint.log output.xml flake8.log tests.log \
		test-result.xml htmlcov fab.log .coverage

publish:
	python setup.py register sdist upload

nosetests: remember
	python setup.py nosetests

pep8: remember
	flake8 --max-complexity 12 --exit-zero dirus/*.py tests/*.py

flake8: pep8

lint: remember
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		-r n dirus/*.py tests/*.py || exit 0

pylint: lint

test: lint pep8 nosetests
