convert: emblem.pdf

%.pdf: %.svg
	inkscape --export-area-drawing --export-text-to-path --without-gui \
	  --export-pdf=$(shell pwd)/$@ --file=$(shell pwd)/$<

%.pdf: %.tif
	convert PixelsPerInch -density 300 $< $@

.PHONY: convert
