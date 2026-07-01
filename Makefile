PYTHON := python3
MAIN := a_maze_ing.py
CONFIG := config.txt

.PHONY: install run debug clean lint lint-strict test package

install:
	$(PYTHON) -c "import flake8, mypy, pytest, setuptools, wheel" || \
		{ $(PYTHON) -m pip install flake8 mypy pytest setuptools wheel; \
		$(PYTHON) -c "import flake8, mypy, pytest, setuptools, wheel"; }

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

package:
	$(PYTHON) setup.py sdist --dist-dir . bdist_wheel --dist-dir .
	rm -rf build mazegen.egg-info
