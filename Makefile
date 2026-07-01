PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt

.PHONY: install run debug clean lint lint-strict test

install:
	$(PYTHON) -m pip show flake8 mypy pytest >/dev/null || \
		$(PYTHON) -m pip install flake8 mypy pytest

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

test:
	$(PYTHON) -m pytest
