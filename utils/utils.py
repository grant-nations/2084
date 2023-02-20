import os
import pygame
from typing import Tuple


def load_font(font_dir: str, font_name: str, size: int) -> pygame.font.Font:
    """
    Load a font from the given file name and return it

    :param font_dir: The directory where the font is located
    :param font_name: The name of the font file
    :param size: The size of the font

    :return: The font
    """
    pygame.font.init()
    font_path = os.path.join(font_dir, font_name)
    return pygame.font.Font(font_path, size)


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
