#! /bin/bash
NAME="multigroup_paper"
latex ${NAME}.tex 
bibtex ${NAME}.aux 
latex ${NAME}.tex 
latex ${NAME}.tex 
dvipdf ${NAME}.dvi

