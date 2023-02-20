from pygame.sprite import Sprite
from utils.thruster_utils import load_thrust_images, LEFT_THRUST, RIGHT_THRUST, VERTICAL_THRUST


class Thruster(Sprite):
    """A class to represent a thruster on a spaceship"""

    def __init__(self,
                 centerx: int,
                 y: int,
                 data_dir: str,
                 inverted: bool = False) -> None:
        """
        :param centerx: The x coordinate of the center of the thruster
        :param y: The y coordinate of the thruster
        :param data_dir: The directory where the thruster images are located
        :param inverted: True if the thruster is inverted (for enemy ships)
        """

        Sprite.__init__(self)
        self.is_alive = True
        self.left_thrust = load_thrust_images(thrust_type=LEFT_THRUST,
                                              image_dir=data_dir,
                                              inverted=inverted)
        self.right_thrust = load_thrust_images(thrust_type=RIGHT_THRUST,
                                               image_dir=data_dir,
                                               inverted=inverted)
        self.vertical_thrust = load_thrust_images(thrust_type=VERTICAL_THRUST,
                                                  image_dir=data_dir,
                                                  inverted=inverted)
        self.image = self.vertical_thrust[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.image_index = 0
        self.direction = VERTICAL_THRUST

        if inverted:
            # self.thrust_offset_x = 0
            self.rect.bottom = y
        else:
            self.rect.y = y

    def animate(self, direction: str, offset_x: int = 0) -> None:
        """Animate the thruster based on the direction of the ship

        :param direction: The direction of the ship
        :param offset_x: The offset to apply to the x coordinate of the thruster
        """

        if direction != self.direction:
            self.direction = direction
            self.image_index = 0

        self.image_index = (self.image_index + 1) % 3

        if self.direction == LEFT_THRUST:
            self.rect.centerx = self.rect.centerx + offset_x
            self.image = self.left_thrust[self.image_index]
        elif self.direction == RIGHT_THRUST:
            self.rect.centerx = self.rect.centerx - offset_x
            self.image = self.right_thrust[self.image_index]
        else:
            self.image = self.vertical_thrust[self.image_index]
