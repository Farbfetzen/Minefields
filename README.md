# Minefields

This is a clone of minesweeper written in Python with Pygame.

![screenshot](/resources/readme_screenshot.png)

## How to run

You need Python 3 and Pygame. Run main.py from inside the source directory so it can find the resource files.

## Controls

- Left click to uncover tiles.
- Right click to mark a tile:
    - The first click places a flag.
    - The second click replaces it with a questionmark.
    - The third click removes the question mark.
- If the number on an uncovered tile equals the number of flagged neighboring tiles then you can double click to reveal all unmarked neighbors.
- Note that marked tiles (either with a flag or a question mark) cannot be uncovered.

## Info

This project is licensed under the MIT license. See file LICENSE for details. All graphics made by me using [Pyxel Edit](http://pyxeledit.com). The font freesansbold.ttf which comes with pygame is licensed under the GNU GPLv3 with a font exception.
