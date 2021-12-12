import pygame as pg

class Camera:
    def __init__(self, width: int, height:int, center: pg.math.Vector2) -> None:
        self.width = width
        self.height = height
        self.center = center
        self.rect = pg.Rect (center, (width, height))
        self.shift = pg.math.Vector2 ((0, 0))

    def apply_shift (self, other):
        x = other[0] + self.shift.x
        y = other[1] + self.shift.y
        return (x, y, other[2])

    def set_shift (self, shift: pg.math.Vector2):
        self.shift = shift