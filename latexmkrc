$out_dir = 'build';

$pdf_mode = 1;
$pdflatex = 'lualatex -synctex=1 -interaction=nonstopmode -shell-escape -output-directory=build %O %S';

$bibtex_use = 1;
$pdf_previewer = 'open';

@default_files = ('main.tex');

$hash_calc_ignore_pattern{'pdf'} = '^/CreationDate |^/ModDate |^/ID \\[<';
