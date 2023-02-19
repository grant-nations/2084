from utils.main_utils import load_image
from pygame.sprite import Sprite

PLAYER_IMG_FILE = "player.png"
PLAYER_WIDTH = PLAYER_HEIGHT = 48

PLAYER_LEFT = 0
PLAYER_RIGHT = 1


class Player(Sprite):

    def __init__(self,
                 x: int,
                 y: int,
                 data_dir: str):
        Sprite.__init__(self)
        self.image = load_image(image_dir=data_dir,
                                img_name=PLAYER_IMG_FILE,
                                colorkey=-1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sound = None  # TODO: Load the sound
        self.firing = False
        self.is_alive = True

    def update(self):

        if not self.is_alive:
            self.kill()

    def move(self,
             direction: str,
             screen_width: int):
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

    def shoot_laser(self):
        """Shoot a laser in the UP direction"""

        self.firing = True

    def die(self):
        """Kill the player"""

        self.is_alive = False
