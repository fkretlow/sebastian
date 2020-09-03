PY=python3

.PHONY: build

build:
	@echo "Generating SMuFL font and metadata in ./build/..."
	@mkdir -p ./build/
	@rm -rf ./build/*
	@$(PY) ./scripts/build.py
