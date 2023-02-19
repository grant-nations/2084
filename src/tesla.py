from pygame.sprite import Sprite
from utils.main_utils import load_image
from utils.tesla_utils import MODEL_3_IMAGE
import random

TESLA_WIDTH = TESLA_HEIGHT = 48


class Tesla(Sprite):
    """Tesla is the base class for all Tesla spaceships"""

    def __init__(self):
        Sprite.__init__(self)
        self.firing = False
        self.is_alive = True
        self.reverse = False

        # The below attributes are set in subclasses
        self.image = None
        self.rect = None
        self.speed = None
        self.laser_cool_down = None
        self.laser_counter = None
        self.laser_timer = None

    def mark_for_deletion(self):
        """Mark the Tesla for deletion"""
        self.is_alive = False

    def shoot_laser(self):
        """Shoot a laser"""
        self.firing = True

    def update(self):
        """Update the Tesla"""

        if not self.is_alive:
            self.kill()

        self.move()

        if self.laser_counter == self.laser_timer:
            self.shoot_laser()
            self.laser_counter = 0
            self.laser_timer = random.randint(1, self.laser_cool_down)
        else:
            self.laser_counter += 1

    def move(self) -> None:

        x_speed = self.speed
        if self.reverse:
            x_speed *= -1

        self.rect.x += x_speed

    def reverse_direction(self):
        self.reverse = not self.reverse

    def move_down(self):
        self.rect.y += self.speed


class ModelS(Tesla):
    """Model S is the fastest Tesla"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 4


class Model3(Tesla):
    """Model 3 is the second slowest Tesla"""

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str):
        Tesla.__init__(self)
        self.image = load_image(image_dir=data_dir,
                                img_name=MODEL_3_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.laser_cool_down = 700  # frames
        self.laser_counter = 0
        self.laser_timer = random.randint(1, self.laser_cool_down)


class ModelX(Tesla):
    """Model X is the slowest Tesla"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 1


class ModelY(Tesla):
    """Model Y is the second fastest Tesla"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 3
