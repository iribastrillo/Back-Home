import sys, random
import itertools as it

import pygame as pg
from pygame.locals import *

from entities import Avatar, PhysicsBody, Vehicle, Astro
from camera import Camera
from ux import Cursor
from states import game_state
from app import App


WIDTH = 640
HEIGHT = 400

pg.init ()
pg.display.set_caption ('Rotar imagen')
clock = pg.time.Clock ()
screen = pg.display.set_mode ((WIDTH, HEIGHT))


#Player setup
player_image = pg.image.load ('queen.png')
player_body = PhysicsBody ()
player_vehicle = Vehicle(player_body)
player = Avatar (player_image, player_body, player_vehicle)
single_player = pg.sprite.GroupSingle ()
single_player.add(player)



#Camera setup
camera = Camera (100, 100, pg.math.Vector2(WIDTH/2 - 50, HEIGHT/2 - 50))

#UX setup
cursor = Cursor (pg.math.Vector2 ((320, 200)), pg.math.Vector2 ((320, 200)))

#World setup
entity = (200, 200, 40)

astros = pg.sprite.Group ()

for i in it.repeat (None, 15):
    radius = random.randint (1, 30)
    surf = pg.Surface ((radius*2, radius*2), depth=32)
    x = random.randint (-640, 640)
    y = random.randint (-400, 400)
    image = pg.draw.circle (surf, (40, random.randint (1, 255), 255), (radius, radius), radius)
    astro = Astro (surf, PhysicsBody ())
    astro.rect = surf.get_rect (center=(x, y))
    astros.add (astro)

while True:

    screen.fill ((10, 10, 25))

    player.vehicle.set_target(cursor.global_coordinates)

    if (player.moving):
        rotor = player.body.screen_coordinates - cursor.global_coordinates
        player.body.angle = rotor.angle_to(pg.math.Vector2 (0, 1))

    player.image, player.rect = player.draw()

     
    # SHIFT PHASE
    camera.set_shift (pg.math.Vector2 (
        player.body.velocity.x * -1, 
        player.body.velocity.y * -1)
    )


    cursor.global_coordinates += player.body.velocity * -1

    # for other in astros:
    #     rect = other.rect
    #     other.rect.x = rect.x + camera.shift.x
    #     other.rect.y = rect.y + camera.shift.y
    #     print (other.rect)

    entity = camera.apply_shift(entity)

    # DRAWING PHASE
    pg.draw.rect (screen, (20, 20, 40, ), camera.rect)
    planet = pg.draw.circle (screen, (255, 100, 255), (entity[0], entity[1]), entity[2])
    single_player.draw(screen)
    astros.draw (screen)
    astros.update()
    single_player.update()


    if (player.collidecirc(planet)):
        pg.draw.circle (screen, (255, 0, 0), player.body.screen_coordinates, 5)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit ()
            sys.exit ()
        if event.type == MOUSEBUTTONDOWN:
            cursor.global_coordinates = pg.mouse.get_pos()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                pass
                #player.rotate (-10)
            if event.key == K_LEFT:
                pass
                #player.rotate (10)

    pg.display.update ()
    clock.tick (60)