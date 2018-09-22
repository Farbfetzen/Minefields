# Minefields

This is a clone of the popular game minesweeper.

![screenshot](/resources/screenshot.png)

## How to run

You need Python 3 and PyGame. Run main.py from inside the source directory so it can find the resource files. I recommend installing PyGame in a virtual environment, for example Pipenv.  
`cd source`  
`pipenv run python main.py`

## Controls

- Left click to uncover tiles.
- Right click to mark a tile:
    - The first click places a flag.
    - The second click replaces it with a questionmark.
    - The third click removes the question mark.
- If the number on an uncovered tile equals the number of flagged neighboring tiles then you can use a double click to reveal all unmarked neighbors.
- Note that marked tiles (either with a flag or a question mark) cannot be uncovered.

## Info

Written in Python 3 using PyGame.  
All graphics made by me using [Pyxel Edit](http://pyxeledit.com).  
The font used is the standard pygame font.
