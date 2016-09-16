PYTHON=python3 -m


all:
	$(PYTHON) symbiotic locate lucas

pr:
	$(PYTHON) symbiotic locate printer

news:
	$(PYTHON) symbiotic news 10

validate:
	$(PYTHON) symbiotic validate


t: test
test:
	pytest symbiotic --doctest-module
