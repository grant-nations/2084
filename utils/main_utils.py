import os
import pygame
from typing import Tuple

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def load_image(image_dir: str,
               img_name: str,
               colorkey: Tuple[int, int, int] = None,
               scale: int = 1) -> pygame.Surface:
    """
    Load an image from the given file name and return it

    :param data_dir: The directory where the image is located
    :param img_name: The name of the image file
    :param colorkey: The color to use as the transparent color
    :param scale: The scale to apply to the image

    :return: The image and its rectangle
    """

    img_path = os.path.join(image_dir, img_name)
    img = pygame.image.load(img_path).convert_alpha()

    size = img.get_size()
    size = (size[0] * scale, size[1] * scale)
    img = pygame.transform.scale(img, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, pygame.RLEACCEL)

    return img


def load_sound(sound_dir: str, sound_name: str) -> pygame.mixer.Sound:
    """
    Load a sound from the given file name and return it

    :param sound_dir: The directory where the sound is located
    :param sound_name: The name of the sound file

    :return: The sound
    """

    sound_path = os.path.join(sound_dir, sound_name)
    return pygame.mixer.Sound(sound_path)


def explode(screen: pygame.Surface,
            x: int,
            y: int,
            data_dir: str):
    """
    Play the explosion animation at the given location

    :param screen: The screen to draw the explosion on
    :param x: The x coordinate of the explosion
    :param y: The y coordinate of the explosion
    :param data_dir: The directory where the explosion images are located
    """

    explosion_images = []
    for i in range(1, 9):
        img_name = f"explosion{i}.png"
        img = load_image(image_dir=data_dir,
                         img_name=img_name,
                         colorkey=-1,
                         scale=2)
        explosion_images.append(img)

    for img in explosion_images:
        screen.blit(img, (x, y))
        pygame.display.flip()
        pygame.time.delay(50)
