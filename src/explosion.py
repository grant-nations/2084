from pygame.sprite import Sprite
from utils.explosion_utils import get_images
from typing import Tuple


class Explosion(Sprite):
    """Explosion is the base class for all explosions"""

    def __init__(self,
                 center: Tuple[int, int],
                 data_dir: str):
        Sprite.__init__(self)
        self.is_alive = True
        self.images = get_images(data_dir=data_dir)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image_index = 0

    def update(self):
        """Update the explosion"""
        self.image_index += 1

        if self.image_index >= len(self.images):
            self.kill()
            return

        self.image = self.images[self.image_index]
