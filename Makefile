all: clean venv test sdist

clean:
	find lento_dvd -type f -name *.pyc | xargs rm -rf
	find lento_dvd -type d -name __pycache__ | xargs rm -rf
	rm -rf coverage
	rm -f .coverage
	rm -rf dist
	rm -f MANIFEST
	rm -rf lento_dvd.egg-info/
	rm -f ~/.lento_dvd

venv2:
	rm -rf ./.venv/
	virtualenv --python=python2.7 --system-site-packages .venv
	.venv/bin/pip install nose==1.3.3 coverage==3.7.1 mock==1.0.1

venv3:
	rm -rf ./.venv3/
	virtualenv --python=python3 --system-site-packages .venv3
	.venv3/bin/pip install nose==1.3.3 coverage==3.7.1 mock==1.0.1

venv: venv2 venv3

test2:
	.venv/bin/nosetests

test3:
	.venv3/bin/nosetests

test: test2 test3

cover:
	export .venv3/bin/nosetests --with-coverage --cover-branches --cover-package=lento_dvd --cover-html --cover-html-dir=coverage

run:
	bin/lento_dvd

doc:
	rm -f README
	pandoc README.md -o README -w rst

sdist2: clean doc
	python2.7 setup.py sdist

sdist3: clean doc
	python3 setup.py sdist

sdist: sdist2 sdist3

install: sdist2
	pip install dist/lento_dvd-*.tar.gz
	rm -rf dist

uninstall:
	pip uninstall lento_dvd
