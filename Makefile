.PHONY: test

test:
	pytest -xv ./tests/test_functional.py

unit:
	pytest -xv ./tests/test_starch2.py

build:
	chmod +x ./starch2/starch2.py
	cp ./starch2/starch2.py ~/bin