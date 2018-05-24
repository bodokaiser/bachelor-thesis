MAIN=main

TARGET=$(MAIN).pdf

BUILD_DIR=build

LATEXMK=lualatex -output-directory $(BUILD_DIR) -deps

DEPS=$(wildcard *.tex)
DEPS+=$(wildcard *.bib)

build:
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(MAIN).tex

clean:
	rm -rf $(TARGET) $(TMP_DIR)

.PHONY: build clean
