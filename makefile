.PHONY: install tests

install:
	./install.sh

tests:
	python3 -m unittest discover
	bash test/test_stdin.sh
