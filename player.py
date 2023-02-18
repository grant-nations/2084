from utils import LEFT, RIGHT


class Player(object):

    def __init__(self,
                 id: int,
                 x: int,
                 y: int):
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.alive = True
        self.firing = False

    def move(self, direction: str):
        """Move the player in the given direction"""

        if direction == LEFT:
            self.x -= 1
        elif direction == RIGHT:
            self.x += 1

    def shoot_laser(self):
        """Shoot a laser in the given direction"""

        self.firing = True

    def die(self):
        """Pretty self explanatory"""

        self.alive = False
