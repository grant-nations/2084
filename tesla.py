from utils import UP, DOWN, LEFT, RIGHT


class Tesla(object):
    """Tesla is the base class for all Tesla cars"""

    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.x = 0
        self.y = 0
        self.alive = True
        self.firing = False
        self.speed = None  # this will be set in the subclasses

    def move(self, direction: str):
        """Move the Tesla in the given direction"""

        if direction == UP:
            self.y += self.speed
        elif direction == DOWN:
            self.y -= self.speed
        elif direction == LEFT:
            self.x -= self.speed
        elif direction == RIGHT:
            self.x += self.speed

    def shoot_laser(self, direction: str):
        """Shoot a laser in the given direction"""
        self.firing = True

    def get_hit(self):
        """Get hit by a laser"""

        self.health -= 1
        if self.health <= 0:
            self.alive = False


class ModelS(Tesla):
    """Model S is the fastest Tesla, but has the lowest health"""

    def __init__(self, id: int):
        super().__init__(id)
        self.speed = 4
        self.health = 1


class Model3(Tesla):
    """Model 3 is the second slowest Tesla, but has the second highest health"""

    def __init__(self, id: int):
        super().__init__(id)
        self.speed = 2
        self.health = 3


class ModelX(Tesla):
    """Model X is the slowest Tesla, but has the highest health"""

    def __init__(self, id: int):
        super().__init__(id)
        self.speed = 1
        self.health = 4


class ModelY(Tesla):
    """Model Y is the second fastest Tesla, but has the second lowest health"""

    def __init__(self, id: int):
        super().__init__(id)
        self.speed = 3
        self.health = 2
