Agar.io Clone - Python Game
Description

This is a simple clone of the popular Agar.io game built using Python and the Pygame library. In this game, players control a circular cell that grows in size by consuming smaller cells scattered across the map. The goal is to grow larger by eating cells while avoiding being eaten by larger cells.

Features

Randomly scattered food (cells) across the map.
Player-controlled cell that moves toward the mouse pointer.
Cell growth system as you consume smaller cells.
Barriers at the edges of the screen to prevent the player from moving off-screen.
Dynamic camera that follows the player, zooming in and out based on the player's size.
Simple HUD displaying the player's score (mass).
Requirements
Python 3.x
Pygame library

Installation

Make sure you have Python 3.x installed on your computer.

Install the Pygame library if you don't have it installed:

pip install pygame

Download or clone this repository to your local machine.

Run the game by executing the following command in the terminal:

python agar.py

Controls

Mouse: Move the player cell by moving the mouse pointer.
ESC: Exit the game.
WASD: Use WASD keys to move the player cell.

How It Works

Key Components
Grid: Represents the background grid of the game. It is drawn using horizontal and vertical lines.
Camera: Used to adjust the player's point of view, zooming in and out based on the player's size.
Player: The cell controlled by the player. It moves towards the mouse pointer and grows by consuming smaller cells.
Cells (Food): Randomly scattered objects that the player can consume to grow in size.
Barriers: Black borders placed at the edges of the screen to prevent the player from moving outside the grid.
HUD: Displays the player's score, which is based on the mass of the player's cell.
Player Movement
The player's cell moves towards the mouse pointer. The movement speed is scaled based on the player's current size. The player grows in size as they consume smaller cells.

Acknowledgements
Thanks to the Pygame library for making game development easy with Python.
Thanks to the original Agar.io game for the inspiration behind this clone.
