MAIN=main
TARGET=$(MAIN).pdf

IMG_DIR=images
TMP_DIR=build
PWD_DIR:=$(shell pwd)

LATEXMK=latexmk -lualatex -auxdir=$(TMP_DIR) -outdir=$(TMP_DIR) \
  -deps -bibtex --shell-escape -use-make

SVG=$(wildcard images/*.svg)
IMG=$(SVG)

build: $(TARGET)

%.pdf: $(TMP_DIR)/%.pdf
	ln -f $(TMP_DIR)/$@ .

$(TMP_DIR)/%.pdf: %.tex $(IMG)
	@mkdir -p $(TMP_DIR)
	$(LATEXMK) $(MAIN).tex

$(TMP_DIR)/%.pdf: $(IMG_DIR)/%.svg
	inkscape --export-area-drawing --export-text-to-path --without-gui \
	  --export-pdf=$(PWD_DIR)/$@ --file=$(PWD_DIR)/$<

clean:
	rm -rf $(TARGET) $(TMP_DIR)

.PHONY: build clean
