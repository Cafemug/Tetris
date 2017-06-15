from random import randrange as rand
import pygame, sys
import os

caption = 'Tetris'

blockSize = 25
FPS = 30
rows = 22
cols = 16
side_space = 8

colors = [
    [0,0,0],
    [0,0,0],
    [204, 0, 55],
    [255, 51, 0],
    [51, 204, 51],
    [51, 204, 255],
    [255, 255, 77],
    [210, 121, 121],
    [255,0,255]
]

pieces = [
    [[8],
     [8],
     [8],
     [8]],

    [[2,2,2],
     [0,2,0]],

    [[3,3,0],
     [0,3,3]],

    [[4,0,0],
     [4,4,4]],

    [[5,5],
     [5,5]],

    [[0,6,6],
     [6,6,0]],

    [[0,0,7],
     [7,7,7]],
]

small_font_size = 25
big_font_size = 40

level_scores = [0, 200, 400, 800, 1600, 3200, 10000000]
