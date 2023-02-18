from tesla import Tesla
from player import Player
from laser import Laser


class Space(object):
    """Space is the class that represents the space that the Teslas and the player are in"""

    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height

    def in_view(self, x: int, y: int):
        """Return True if the given position is in the view of the game space"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_new_id(self):
        """Return a new unique id"""
        pass

    def add_tesla(self, tesla: Tesla):
        """Add the given Tesla to the space"""
        pass

    def add_player(self, player: Player):
        """Add the given player to the space"""
        pass

    def add_laser(self, laser: Laser):
        """Add the given laser to the space"""
        pass
