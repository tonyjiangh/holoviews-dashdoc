#!/bin/sh

# Create the doc folder and Info.plist in advance
wget --execute="robots = off" --mirror --convert-links --no-parent --wait=5 http://holoviews.org/Reference_Manual/index.html
rm -rf holoviews.docset/Contents/Resources/Documents/*
mv -r holoviews.org/Reference_Manual holoviews.docset/Contents/Resources/Documents/
rm -rf holoviews.org

python hvdoc2set.py
