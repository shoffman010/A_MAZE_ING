PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt

.PHONY: install run debug clean lint lint-strict test package

install:
	$(PYTHON) -c "import build, flake8, mypy, pytest" || \
		{ $(PYTHON) -m pip install build flake8 mypy pytest; \
		$(PYTHON) -c "import build, flake8, mypy, pytest"; }

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage build dist *.egg-info

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
