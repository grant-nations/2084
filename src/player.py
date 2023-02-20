from utils.utils import load_image
from pygame.sprite import Sprite
from src.thruster import Thruster

PLAYER_IMG_FILE = "player.png"
PLAYER_WIDTH = PLAYER_HEIGHT = 48

PLAYER_LEFT = 0
PLAYER_RIGHT = 1
PLAYER_VERTICAL = 2


class Player(Sprite):

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str) -> None:
        """
        :param x: The x coordinate of the player
        :param y: The y coordinate of the player
        :param data_dir: The directory containing the player image
        """

        Sprite.__init__(self)
        self.image = load_image(image_dir=data_dir,
                                img_name=PLAYER_IMG_FILE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.firing = False
        self.is_alive = True
        self.thruster = Thruster(centerx=self.rect.centerx,
                                 y=self.rect.bottom,
                                 data_dir=data_dir)
        self.direction = PLAYER_VERTICAL

    def update(self) -> None:
        """Update the player"""

        if not self.is_alive:
            self.thruster.kill()
            self.kill()

        self.thruster.rect.centerx = self.rect.centerx
        self.thruster.rect.y = self.rect.bottom
        self.thruster.animate(direction=self.direction, offset_x=3)

    def set_direction(self, direction: int) -> None:
        """
        Set the direction of the player

        :param direction: The direction to set the player to
        """
        self.direction = direction

    def move(self,
             direction: str,
             screen_width: int) -> None:
        """
        Move the player in the given direction

        :param direction: The direction to move the player in
        :param screen_width: The width of the screen
        """
        if direction == PLAYER_LEFT:
            self.rect.x -= 5
        elif direction == PLAYER_RIGHT:
            self.rect.x += 5

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen_width - PLAYER_WIDTH:
            self.rect.x = screen_width - PLAYER_WIDTH

    def shoot_laser(self) -> None:
        """Shoot a laser in the UP direction"""

        self.firing = True

    def die(self):
        """Pretty self explanatory"""

        self.is_alive = False
