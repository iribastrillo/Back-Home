import pygame as pg

from camera import Camera

from entities import Avatar

FPS = 60
WIDTH = 640
HEIGHT = 400

class App:
    def __init__(self, camera: Camera, state) -> None:
        self.running = True
        self.camera = camera
        self.state = state
        self.screen = pg.display.set_mode ((WIDTH, HEIGHT))
        self.clock = pg.time.Clock ()
        self.single = pg.sprite.GroupSingle ()
        self.FPS = FPS
        self.entities = pg.sprite.Group ()
        self.clock = pg.time.Clock ()
        self.cursor = None

        pg.display.set_caption ('Back Home')

    def add_player (self, player: Avatar) -> None:
        self.single.add (player)

    def add_entities (self, entities) -> None:
        for e in entities:
            self.entities.add (e)

    def set_cursor (self, cursor):
        self.cursor = cursor

    def run (self) -> None:
        self.state (self)