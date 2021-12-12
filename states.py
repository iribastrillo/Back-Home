import sys

import pygame as pg
from pygame.locals import *

entity = (200, 200, 20)

def game_state (app):
    while True:

        app.screen.fill ((10, 10, 25))

        cursor = app.cursor
        player = app.single.sprite 
        camera = app.camera
        screen = app.screen
        entities = app.entities

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

        for other in entities:
            rect = other.rect
            other.rect.x = rect.x + camera.shift.x
            other.rect.y = rect.y + camera.shift.y
            print (other.rect)


        entity = camera.apply_shift(entity)

        # DRAWING PHASE
        pg.draw.rect (screen, (20, 20, 40, ), camera.rect)
        planet = pg.draw.circle (screen, (255, 100, 255), (entity[0], entity[1]), entity[2])
        app.single.draw(screen)
        entities.draw (screen)
        app.single.update()
        entities.update() 


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
        app.clock.tick (app.FPS)