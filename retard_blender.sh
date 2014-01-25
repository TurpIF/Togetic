#!/bin/sh
cat donnees_capteur/retard_blender.dat | grep -v "[a-zA-Z]" | awk '{print NR" "$1}' | python2 Plot/xyplot.py
