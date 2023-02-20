from pygame.sprite import Sprite
from utils.projectile_utils import get_speed, load_images, MISSILE


PROJECTILE_UP = 0
PROJECTILE_DOWN = 1


class Projectile(Sprite):

    def __init__(self,
                 centerx: int,
                 y: int,
                 direction: str,
                 data_dir: str,
                 projectile_type: str):
        Sprite.__init__(self)
        self.images = load_images(projectile_type=projectile_type,
                                  image_dir=data_dir)
        self.projectile_type = projectile_type
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.y = y
        self.direction = direction
        self.is_alive = True
        self.image_index = 0
        self.speed = get_speed(projectile_type)

    def mark_for_deletion(self):
        """Mark the laser for deletion"""

        self.is_alive = False

    def update(self):
        """Update the laser"""

        if not self.is_alive:
            self.kill()

        self.move()

        if self.projectile_type == MISSILE:
            self.animate_missile()
        else:
            self.animate()

    def animate_missile(self):
        """Animate the missile"""

        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]

    def animate(self):
        """Animate the projectile"""

        if self.image_index == len(self.images) - 1:
            return

        self.image_index += 1
        self.image = self.images[self.image_index]

    def move(self):
        """Move the laser in the given direction"""

        if self.direction == PROJECTILE_UP:
            self.rect.y -= self.speed

        elif self.direction == PROJECTILE_DOWN:
            self.rect.y += self.speed
