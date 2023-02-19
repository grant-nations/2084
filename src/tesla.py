from pygame.sprite import Sprite
from utils.utils import load_image
from src.projectile import Projectile, PROJECTILE_DOWN
from utils.projectile_utils import GREEN_LASER, RED_LASER, BLUE_LASER
import random

TESLA_WIDTH = TESLA_HEIGHT = 48
PROTO_3_IMAGE = 'red_03.png'
PROTO_S_IMAGE = 'red_01.png'
LEFT = -1
RIGHT = 1


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
        self.points = None
        self.laser = None

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

        pass


class ProtoS(Tesla):
    """Model S is the fastest Tesla"""

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str,
                 move_direction: int = RIGHT):
        Tesla.__init__(self)
        self.speed = 1
        self.points = 80
        self.image = load_image(image_dir=data_dir,
                                img_name=PROTO_S_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.laser_cool_down = 60  # frames
        self.laser_counter = 0
        self.laser_timer = random.randint(1, self.laser_cool_down)
        self.move_direction = move_direction
        self.laser = Projectile(centerx=self.rect.centerx,
                                y=self.rect.bottom,
                                direction=PROJECTILE_DOWN,
                                data_dir=data_dir,
                                laser_type=GREEN_LASER)

    def get_laser(self,
                  data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          laser_type=GREEN_LASER)

    def move(self) -> None:
        x_speed = self.speed

        if self.reverse:
            x_speed *= -1

        x_velocity = 2 * x_speed * self.move_direction

        self.rect.x += x_velocity
        self.rect.y += self.speed

    def reverse_direction(self):
        self.reverse = not self.reverse


class Proto3(Tesla):
    """Model 3 is the second slowest Tesla"""

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str):
        Tesla.__init__(self)
        self.image = load_image(image_dir=data_dir,
                                img_name=PROTO_3_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.laser_cool_down = 1000  # frames
        self.laser_counter = 0
        self.laser_timer = random.randint(1, self.laser_cool_down)
        self.points = 10

    def get_laser(self,
                  data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          laser_type=RED_LASER)

    def move(self) -> None:

        x_speed = self.speed
        if self.reverse:
            x_speed *= -1

        self.rect.x += x_speed

    def reverse_direction(self):
        self.reverse = not self.reverse

    def move_down(self):
        self.rect.y += self.speed


class ProtoX(Tesla):
    """Model X is the slowest Tesla"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 1
        self.points = 30


class ProtoY(Tesla):
    """Model Y is the second fastest Tesla"""

    def __init__(self):
        Tesla.__init__(self)
        self.speed = 3
        self.points = 50
