import pygame

pygame.init()

#colors
red = (178, 34, 34)
black = (0, 0, 0)
green = (0, 128, 0)
white = (255, 255, 255)
purple = (148, 0, 211)
yellow = (255, 255, 0)
blue = (0,191,255)

#fonts
tetrisFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
basicFont = pygame.font.Font("OpenSans-Regular.ttf", 12)

#sizes and dimensions
start, end = 100, 300
frame_edge = 2
title_height = 180
playground_size = pg_width, pg_height = 204, 454 #354
y_bottom = title_height + pg_height - frame_edge #532
tile_size = 25
screen_size = width, height = 400, 700 #600
playground_origin = pg_x, pg_y = (width - pg_width) / 2, title_height

