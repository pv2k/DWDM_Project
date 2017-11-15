#!/usr/bin/env bash
c="_text"
i="PAKDD-3year"
j="./Text/"
echo "Opening pdf folder: " $i
echo "pdf_text folder:Text"
mkdir -p Text

for k in ./$i/*.pdf
do
    pdfname="$(echo $k | rev | cut -d "/" -f 1 | rev)"
    echo $j$pdfname$c
    python pdf2txt.py -o "$j$pdfname$c" -t text "$k"
    echo "Converting :"  $pdfname
done
