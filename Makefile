PYTHON=python3 -m


all:
	$(PYTHON) symbiotic locate lucas

pr:
	$(PYTHON) symbiotic locate printer

news:
	$(PYTHON) symbiotic news


t: test
test:
	pytest symbiotic --doctest-module
