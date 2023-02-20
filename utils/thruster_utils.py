from utils.utils import load_image
from typing import List
from pygame import Surface
from pygame.transform import flip

LEFT_THRUST = 0
RIGHT_THRUST = 1
VERTICAL_THRUST = 2


def load_thrust_images(thrust_type: int,
                       image_dir: str,
                       inverted: bool = False) -> List[Surface]:
    """
    Load the images for the laser

    :param thrust_type: The type of thrust to load
    :param image_dir: The directory where the images are located
    :param inverted: True if the thruster is inverted (for enemy ships)

    :return: A list of images
    """

    prefix = ''
    if thrust_type == LEFT_THRUST or thrust_type == RIGHT_THRUST:
        prefix = 'diagonal-thrust-'
    elif thrust_type == VERTICAL_THRUST:
        prefix = 'vertical-thrust-'

    images = []

    for i in range(1, 4):
        index = f'{i}' if i > 9 else f'0{i}'

        img_name = f'{prefix}{index}.png'
        images.append(load_image(image_dir=image_dir,
                                 img_name=img_name,
                                 colorkey=-1))

    if thrust_type == LEFT_THRUST:
        for i, _ in enumerate(images):
            images[i] = flip(images[i], True, False)

    if inverted:
        for i, _ in enumerate(images):
            images[i] = flip(images[i], False, True)

    return images
