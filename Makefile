PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt

.DEFAULT_GOAL := all
.PHONY: all install run debug clean lint lint-strict test package

all: install

install:
	$(PYTHON) -c "import build, flake8, mypy, pytest" || \
		{ $(PYTHON) -m pip install build flake8 mypy pytest; \
		$(PYTHON) -c "import build, flake8, mypy, pytest"; }

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '*.egg-info' -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage build dist

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

test:
	$(PYTHON) -m pytest

package:
	$(PYTHON) -m build
