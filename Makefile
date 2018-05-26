MAIN=main

TARGET=$(MAIN).pdf

IMG_DIR=images
TMP_DIR=build
PWD_DIR=$(shell pwd)

LATEXMK=latexmk -lualatex -auxdir=$(TMP_DIR) -outdir=$(TMP_DIR) \
  -deps -bibtex --shell-escape

DEPS=$(wildcard *.tex)
DEPS+=$(wildcard *.bib)
DEPS+=$(shell find images)

build: $(TARGET)

%.pdf: $(TMP_DIR)/%.pdf
	ln -f $(TMP_DIR)/$@ .

$(TMP_DIR)/%.pdf: %.tex $(DEPS)
	@mkdir -p $(TMP_DIR)
	$(LATEXMK) $(MAIN).tex

$(TMP_DIR)/%.pdf: $(IMG_DIR)/%.svg
	@echo "HOMeBOY\n$(PWD_DIR)"
	inkscape --export-text-to-path --export-area-drawing --export-pdf \
	  $(PWD_DIR)/$@ $(PWD_DIR)/$<

clean:
	rm -rf $(TARGET) $(TMP_DIR)

.PHONY: build clean
