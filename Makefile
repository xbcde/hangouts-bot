.PHONY: install install-windows test lint

install:
	@./scripts/install.sh

install-windows:
	cmd /C "scripts\install.bat"

test:
	pre-commit run --all-files || true
	python3 -m pytest -p no:cacheprovider -x -rP --no-header

lint:
	pre-commit run --all-files
