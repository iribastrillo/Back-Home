import pygame as pg


class Cursor:
    def __init__(self, screen_coordinates: pg.math.Vector2, global_coordinates: pg.math.Vector2) -> None:
        self.screen_coordinates = screen_coordinates
        self.global_coordinates = global_coordinates
    
    def set_global_coordinates (self, coordinates: pg.math.Vector2):
        self.global_coordinates = coordinates