import pygame as pg

def rotate_image (image, rect, angle):
    new_image = pg.transform.rotate (image, angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect

def remap(x, a, b, c, d):
    w =  (x-a) / (b-a)
    y = c + w * (d-c)
    return y