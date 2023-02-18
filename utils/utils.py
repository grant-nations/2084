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
               scale: int = 1) -> Tuple[pygame.Surface, pygame.Rect]:
    """
    Load an image from the given file name and return it

    :param data_dir: The directory where the image is located
    :param img_name: The name of the image file
    :param colorkey: The color to use as the transparent color
    :param scale: The scale to apply to the image

    :return: The image and its rectangle
    """

    img_path = os.path.join(image_dir, img_name)
    img = pygame.image.load(img_path).convert()

    size = img.get_size()
    size = (size[0] * scale, size[1] * scale)
    img = pygame.transform.scale(img, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, pygame.RLEACCEL)

    return img, img.get_rect()


def load_sound(sound_dir: str, sound_name: str) -> pygame.mixer.Sound:
    """
    Load a sound from the given file name and return it

    :param sound_dir: The directory where the sound is located
    :param sound_name: The name of the sound file

    :return: The sound
    """

    sound_path = os.path.join(sound_dir, sound_name)
    return pygame.mixer.Sound(sound_path)
