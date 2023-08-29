.PHONY: test

test:
	pytest -xv ./test.py

build:
	chmod +x ./starch2.py
	cp ./starch2.py ~/bin