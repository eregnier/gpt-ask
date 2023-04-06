ask:
	./venv/bin/python3 main.py
	
install:
	rm -rf venv
	python3 -m virtualenv venv
	./venv/bin/pip install -r requirements.txt

format:
	@black .
