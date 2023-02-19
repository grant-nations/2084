from utils.main_utils import UP, DOWN, LEFT, RIGHT
from pygame.sprite import Sprite
from utils.main_utils import load_image
from utils.tesla_utils import MODEL_3, MODEL_3_IMAGE
import random


class Tesla(Sprite):
    """Tesla is the base class for all Tesla spaceships"""

    def __init__(self):
        Sprite.__init__(self)
        self.firing = False
        self.speed = None  # this will be set in the subclasses
        self.is_alive = True
        self.reverse = False

    def mark_for_deletion(self):
        """Mark the Tesla for deletion"""

        self.death_animation()

    def shoot_laser(self):
        """Shoot a laser"""
        self.firing = True

    def death_animation(self):
        """Play the death animation"""

        # TODO: Play the death animation
        self.is_alive = False


class ModelS(Tesla):
    """Model S is the fastest Tesla, but has the lowest health"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 4
        self.health = 1


class Model3(Tesla):
    """Model 3 is the second slowest Tesla, but has the second highest health"""

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str,):
        Tesla.__init__(self)
        self.image = load_image(image_dir=data_dir,
                                img_name=MODEL_3_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 3
        self.laser_counter = 0
        self.laser_timer = random.randint(1, 600)

    def update(self):
        """Update the Tesla"""

        if not self.is_alive:
            self.kill()

        self.move()

        if self.laser_counter == self.laser_timer:
            self.shoot_laser()
            self.laser_counter = 0
            self.laser_timer = random.randint(1, 700)
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


class ModelX(Tesla):
    """Model X is the slowest Tesla, but has the highest health"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 1
        self.health = 4


class ModelY(Tesla):
    """Model Y is the second fastest Tesla, but has the second lowest health"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 3
        self.health = 2
