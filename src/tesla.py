from pygame.sprite import Sprite
from utils.utils import load_image
from src.projectile import Projectile, PROJECTILE_DOWN
from utils.projectile_utils import GREEN_LASER, RED_LASER, BLUE_LASER, MISSILE
from src.thruster import Thruster
from utils.thruster_utils import VERTICAL_THRUST, LEFT_THRUST, RIGHT_THRUST
import random

TESLA_WIDTH = TESLA_HEIGHT = 48
PROTO_3_IMAGE = 'red_03.png'
PROTO_S_IMAGE = 'orange_04.png'
PROTO_Y_IMAGE = 'green_02.png'
PROTO_X_IMAGE = 'metalic_06.png'

LEFT = -1
RIGHT = 1


class Tesla(Sprite):
    """Tesla is the base class for all Tesla spaceships"""

    def __init__(self):
        Sprite.__init__(self)
        self.firing = False
        self.is_alive = True
        self.reverse = False
        self.thruster = None
        self.direction = VERTICAL_THRUST

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

    def set_direction(self, direction: int):
        """
        Set the direction of the Tesla

        :param direction: The direction to set the Tesla to
        """
        self.direction = direction

    def update(self):
        """Update the Tesla"""

        if not self.is_alive:
            self.kill()
            self.thruster.kill()

        self.move()

        if self.laser_counter == self.laser_timer:
            self.shoot_laser()
            self.laser_counter = 0
            self.laser_timer = random.randint(1, self.laser_cool_down)
        else:
            self.laser_counter += 1

        self.animate()

    def move(self) -> None:

        pass

    def animate(self):
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
        self.thruster = Thruster(centerx=self.rect.centerx,
                                 y=self.rect.top,
                                 data_dir=data_dir,
                                 inverted=True)

    def animate(self):
        self.thruster.rect.centerx = self.rect.centerx
        self.thruster.rect.bottom = self.rect.y + 5
        self.thruster.animate(direction=self.direction, offset_x=5)

    def get_laser(self,
                  data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          projectile_type=GREEN_LASER)

    def move(self) -> None:
        x_speed = self.speed

        if self.reverse:
            x_speed *= -1

        x_velocity = 2 * x_speed * self.move_direction

        self.rect.x += x_velocity
        self.rect.y += self.speed

        if x_velocity < 0:
            self.direction = LEFT_THRUST
        else:
            self.direction = RIGHT_THRUST

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
        self.thruster = Thruster(centerx=self.rect.centerx,
                                 y=self.rect.top,
                                 data_dir=data_dir,
                                 inverted=True)

    def animate(self):
        self.thruster.rect.centerx = self.rect.centerx
        self.thruster.rect.bottom = self.rect.y + 8
        self.thruster.animate(direction=VERTICAL_THRUST)

    def get_laser(self,
                  data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          projectile_type=RED_LASER)

    def move(self) -> None:

        x_speed = self.speed
        if self.reverse:
            x_speed *= -1

        self.rect.x += x_speed

        if x_speed < 0:
            self.direction = LEFT_THRUST
        else:
            self.direction = RIGHT_THRUST

    def reverse_direction(self):
        self.reverse = not self.reverse

    def move_down(self):
        self.direction = VERTICAL_THRUST
        self.rect.y += self.speed


class ProtoX(Tesla):

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str,
                 move_direction: int = VERTICAL_THRUST):
        Tesla.__init__(self)
        self.speed = 1
        self.points = 100

        self.image = load_image(image_dir=data_dir,
                                img_name=PROTO_X_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.laser_cool_down = 10  # frames
        self.laser_counter = 0
        self.laser_timer = 10
        self.move_direction = move_direction
        self.thruster = Thruster(centerx=self.rect.centerx,
                                 y=self.rect.top,
                                 data_dir=data_dir,
                                 inverted=True)

    def animate(self):
        self.thruster.rect.centerx = self.rect.centerx
        self.thruster.rect.bottom = self.rect.y + 5
        self.thruster.animate(direction=self.direction, offset_x=5)

    def get_laser(self, data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          projectile_type=MISSILE)

    def move(self) -> None:

        # perform horizontal movement
        x_speed = self.speed

        if self.reverse:
            x_speed *= -1

        x_velocity = x_speed * self.move_direction

        self.rect.x += x_velocity

        if x_velocity < 0:
            self.direction = LEFT_THRUST
        else:
            self.direction = RIGHT_THRUST

    def reverse_direction(self):
        self.reverse = not self.reverse

    def update(self):

        if not self.is_alive:
            self.kill()
            self.thruster.kill()

        self.move()

        if self.laser_counter == self.laser_timer:
            self.shoot_laser()
            self.laser_counter = 0
            self.laser_timer = self.laser_cool_down
        else:
            self.laser_counter += 1

        self.animate()


class ProtoY(Tesla):
    """Model Y is the second fastest Tesla"""

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str,
                 move_direction: int = VERTICAL_THRUST):
        Tesla.__init__(self)
        self.speed = 2
        self.points = 50

        self.image = load_image(image_dir=data_dir,
                                img_name=PROTO_Y_IMAGE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.laser_cool_down = 60  # frames
        self.laser_counter = 0
        self.laser_timer = random.randint(1, self.laser_cool_down)
        self.move_direction = move_direction
        self.thruster = Thruster(centerx=self.rect.centerx,
                                 y=self.rect.top,
                                 data_dir=data_dir,
                                 inverted=True)

        self.move_y_cooldown = 90  # frames
        self.move_y_timer = random.randint(1, self.move_y_cooldown)
        self.y_move_frames = 5

    def animate(self):
        self.thruster.rect.centerx = self.rect.centerx
        self.thruster.rect.bottom = self.rect.y + 5
        self.thruster.animate(direction=self.direction, offset_x=5)

    def get_laser(self,
                  data_dir: str):

        # TODO: change this to not load from disk every time
        return Projectile(centerx=self.rect.centerx,
                          y=self.rect.bottom,
                          direction=PROJECTILE_DOWN,
                          data_dir=data_dir,
                          projectile_type=BLUE_LASER)

    def move(self) -> None:

        # perform random vertical movement
        if self.y_move_frames > 0:
            self.rect.y += self.speed
            self.y_move_frames -= 1
            return

        if self.move_y_timer == 0:
            self.rect.y += self.speed * 2
            self.move_y_timer = random.randint(1, self.move_y_cooldown)
            self.y_move_frames = 5
            self.direction = VERTICAL_THRUST
            return
        else:
            self.move_y_timer -= 1

        # perform horizontal movement
        x_speed = self.speed

        if self.reverse:
            x_speed *= -1

        x_velocity = x_speed * self.move_direction

        self.rect.x += x_velocity

        if x_velocity < 0:
            self.direction = LEFT_THRUST
        else:
            self.direction = RIGHT_THRUST

    def reverse_direction(self):
        self.reverse = not self.reverse
