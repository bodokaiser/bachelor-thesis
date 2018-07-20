SOURCES := $(shell find . -type f -name '*.tex')
TARGETS := $(SOURCES:.tex=.pdf)

build: clean $(TARGETS)

%.pdf: %.ps
	ps2pdf $< $@

%.ps: %.dvi
	dvips -o $@ $<

%.dvi: %.tex
	latex -output-format=dvi $<

clean:
	rm *.aux *.log

.PHONY: build clean
