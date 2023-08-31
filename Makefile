.PHONY: test

test:
	pytest -xv ./test_functional.py

unit:
	pytest -xv ./test_starch2.py

build:
	chmod +x ./starch2.py
	cp ./starch2.py ~/bin