from tesla import Tesla
from utils.utils import UP, DOWN, LEFT, RIGHT
from player import Player


class Laser(object):
    """
    Laser is the class that represents a laser shot by a Tesla
    and by the player
    """

    def __init__(self,
                 id: int,
                 x: int,
                 y: int,
                 direction: str):
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction

    def move(self):
        """Move the laser in the given direction"""

        if self.direction == UP:
            self.y += 1
        elif self.direction == DOWN:
            self.y -= 1

    def impact(self):
        """Impact the laser on a Tesla or the player"""

        self.alive = False
