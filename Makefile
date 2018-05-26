MAIN=main

TARGET=$(MAIN).pdf

BUILD_DIR=build

LATEXMK=latexmk -lualatex -auxdir=$(BUILD_DIR) -outdir=$(BUILD_DIR) -deps -pdf -bibtex

DEPS=$(wildcard *.tex)
DEPS+=$(wildcard *.bib)

build:
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(MAIN).tex

clean:
	rm -rf $(TARGET) $(TMP_DIR)

.PHONY: build clean
