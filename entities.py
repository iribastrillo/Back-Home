import pygame as pg

from utils import rotate_image, remap


class PhysicsBody:
    def __init__(self) -> None:
        self.screen_coordinates = pg.math.Vector2 ((320, 200))
        self.velocity = pg.math.Vector2 ((0, 0))
        self.acceleration = pg.math.Vector2 ((0, 0))
        self.global_coordinates = pg.math.Vector2 ((320, 200))
        self.mass = 1
        self.angle = 0

    def update (self):
        self.velocity += self.acceleration
        self.global_coordinates += self.velocity
        self.acceleration *= 0


class Vehicle:
    def __init__(self, body: PhysicsBody) -> None:
        self.target = pg.math.Vector2 ((320, 200))
        self.behaviour = None
        self.body = body
        self.max_speed = 4
        self.max_force = 0.1
        
    def apply_force (self, force):
        self.body.acceleration = force/self.body.mass

    def calculate_desired_velocity (self) -> pg.math.Vector2:
        return self.target - self.body.screen_coordinates

    def calculate_distance_to_target (self):
        return self.body.screen_coordinates.distance_to(self.target)

    def calculate_rotor (self):
        ...

    def arrive (self):
        desired = self.calculate_desired_velocity ()
        steer = pg.math.Vector2 ((0, 0))
        distance = self.calculate_distance_to_target ()
        if(desired.length() > 0.01):
            if (distance < 100):
                desired.scale_to_length (remap(distance, 0, 50, 0, self.max_speed))
            else:
                desired.scale_to_length (self.max_speed)
            steer = desired - self.body.velocity
            if (steer.length () > 0.01):  
                steer.scale_to_length (self.max_force)
        return steer

    def seek (self) -> pg.math.Vector2:
        desired = self.calculate_desired_velocity ()
        steer = pg.math.Vector2 ((0, 0))
        if (desired.length () > 0):
            desired.scale_to_length (self.max_speed)
            steer = desired - self.body.velocity
            if (steer.length () > 0.01):
                steer.scale_to_length (self.max_force)
        return steer

    def set_target (self, target: pg.math.Vector2) -> None:
        self.target = target


class Astro (pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, body: PhysicsBody) -> None:
        super().__init__()
        self.image = image
        self.body = body
        self.radius = image.get_width()/2
        self.rect = image.get_rect()


class Avatar (pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, body: PhysicsBody, vehicle: Vehicle) -> None:
        super().__init__()
        self.image = image
        self.original = image
        self.radius = image.get_width()/2
        self.rect = image.get_rect()
        self.colliding = False
        self.moving = False
        self.body = body
        self.vehicle = vehicle

    def draw (self):
        surf, rect = rotate_image (
            self.original, 
            self.original.get_rect(center=self.body.screen_coordinates), 
            self.body.angle
        )
        return surf, rect

    def update (self):
        self.vehicle.apply_force (self.vehicle.arrive())
        self.body.update ()
        self.check_movement ()

    def check_movement (self):
        self.moving = self.body.velocity.length () > 0.1

    def colliderect (self, other) -> bool:
        return self.rect.colliderect (other)

    def collidecirc (self, other) :
        this = pg.math.Vector2 (self.rect.center)
        that = pg.math.Vector2 (other[0] + 40, other[1] +  40)
        return this.distance_to(that) <= self.radius + other[2]/2

    def set_location (self, location: pg.math.Vector2):
        self.body.location = location

    def set_rect (self, rect: pg.Rect):
        self.rect = rect