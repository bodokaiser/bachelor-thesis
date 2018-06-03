MAIN=main

WORK_DIR=$(shell pwd)
BUILD_DIR=build
IMAGE_DIR=images
FIGURE_DIR=figures

LATEX=lualatex
LATEX_OPT=-shell-escape -synctex=1

LATEXMK=latexmk
LATEXMK_OPT=-use-make -lualatex -interaction=nonstopmode -outdir=$(BUILD_DIR)
LATEXMK_OPT_CONT=-pvc

build: $(MAIN).pdf

$(MAIN).pdf: $(BUILD_DIR)/$(MAIN).pdf
	ln -s $< $@

$(BUILD_DIR)/$(MAIN).pdf:
	$(LATEXMK) $(LATEXMK_OPT) \
            -pdflatex="$(LATEX) $(LATEX_OPT) %O %S" $(MAIN)

$(BUILD_DIR)/$(MAIN).gls:
	makeglossaries -d $(BUILD_DIR) $(MAIN)

$(BUILD_DIR)/%.pdf: $(IMAGE_DIR)/%.svg
	inkscape --export-area-drawing --export-text-to-path --without-gui \
	  --export-pdf=$(WORK_DIR)/$@ --file=$(WORK_DIR)/$<

$(BUILD_DIR)/%.pdf: $(IMAGE_DIR)/%.tif
	convert PixelsPerInch -density 300 $< $@

$(BUILD_DIR)/%.pdf: $(IMAGE_DIR)/%.tiff
	convert PixelsPerInch -density 300 $< $@

clean:
	$(LATEXMK) -C
	rm $(BUILD_DIR)/*

.PHONY: clean
