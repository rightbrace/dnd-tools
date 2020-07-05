#!/bin/bash

pandocdir="$HOME/.pandoc/templates"
texdir="$HOME/texmf/tex/latex"

echo "Pandoc: $pandocdir"
echo "Latex: $texdir"

mkdir -p "$pandocdir"
mkdir -p "$texdir"

cp dnd.latex "$pandocdir/"
cp -r DND-5e-LaTeX-Template "$texdir/"
