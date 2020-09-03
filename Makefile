PY=fontforge --script

.PHONY: build

build:
	@echo "Generating SMuFL font and metadata in ./build/..."
	@mkdir -p ./build/
	@rm -rf ./build/*
	$(PY) ./scripts/build.py

rename:
	@echo "Renaming glyphs..."
	$(PY) ./scripts/rename.py
