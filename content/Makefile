LATEX=lualatex
LATEX_OPT=-shell-escape -synctex=1

LATEXMK=latexmk
LATEXMK_OPT=-use-make -lualatex -shell-escape -interaction=nonstopmode -outdir=build
LATEXMK_OPT_CONT=-pvc

build: build/main.pdf

%.pdf:
	$(MAKE) -C ../media
	$(MAKE) -C standalone

main.gls: build/main.gls
main.acr: build/main.acr

build/main.pdf:
	$(LATEXMK) -f $(LATEXMK_OPT) \
            -pdflatex="$(LATEX) $(LATEX_OPT) %O %S" main

build/main.acr build/main.gls:
	makeglossaries -d build main

clean:
	$(LATEXMK) -C
	rm -rf build

.PHONY: build clean
