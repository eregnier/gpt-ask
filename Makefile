.PHONY: build 

install:
	rm -rf venv
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt

format:
	@black .

build:
	./venv/bin/python setup.py sdist
	./venv/bin/python setup.py bdist_wheel

push: build
	./venv/bin/pip install twine
	./venv/bin/twine upload dist/*

clean:
	rm -rf build dist q.egg-info
	find -name *.pyc -delete
	@- git status

deploy: push clean
