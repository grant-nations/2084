from utils.utils import LEFT, RIGHT, load_image
from pygame.sprite import Sprite

PLAYER_IMG_FILE = "player.png"
PLAYER_WIDTH = PLAYER_HEIGHT = 48


class Player(Sprite):

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str):
        Sprite.__init__(self)
        self.image, self.rect = load_image(image_dir=data_dir,
                                           img_name=PLAYER_IMG_FILE,
                                           colorkey=-1)
        self.rect.x = x
        self.rect.y = y
        self.sound = None  # TODO: Load the sound
        self.firing = False

    def move(self, direction: str):
        """
        Move the player in the given direction

        :param direction: The direction to move the player in
        """

        if direction == LEFT:
            self.rect.x -= 5
        elif direction == RIGHT:
            self.rect.x += 5

    def shoot_laser(self):
        """Shoot a laser in the UP direction"""

        self.firing = True
