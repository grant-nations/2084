from utils.utils import load_image
from typing import List
from pygame import Surface


RED_LASER = 'red_laser'
RED_LASER_SPEED = 3
RED_LASER_FILE_PREFIX = 'red_laser_'

BLUE_LASER = 'blue_laser'
BLUE_LASER_SPEED = 7
BLUE_LASER_FILE_PREFIX = 'blue_laser_'

GREEN_LASER = 'green_laser'
GREEN_LASER_SPEED = 5
GREEN_LASER_FILE_PREFIX = 'green_laser_'

ORANGE_LASER = 'orange_laser'
ORANGE_LASER_SPEED = 10
ORANGE_LASER_FILE_PREFIX = 'orange_laser_'

MISSILE = 'missile'
MISSILE_SPEED = 5
MISSILE_FILE_PREFIX = 'missile-'


def get_projectile_images(projectile_type: str,
                          image_dir: str) -> List[Surface]:
    """
    Load the images for the laser

    :param projectile_type: The type of laser to load
    :param image_dir: The directory where the images are located

    :return: A list of images
    """

    images = []

    file_prefix = ''
    num_images = 3  # number of images for all lasers (not missiles)

    if projectile_type == RED_LASER:
        file_prefix = RED_LASER_FILE_PREFIX
    elif projectile_type == BLUE_LASER:
        file_prefix = BLUE_LASER_FILE_PREFIX
    elif projectile_type == GREEN_LASER:
        file_prefix = GREEN_LASER_FILE_PREFIX
    elif projectile_type == ORANGE_LASER:
        file_prefix = ORANGE_LASER_FILE_PREFIX
    elif projectile_type == MISSILE:
        file_prefix = MISSILE_FILE_PREFIX
        num_images = 2

    for i in range(1, num_images + 1):
        index = f'{i}'

        img_name = f'{file_prefix}{index}.png'
        images.append(load_image(image_dir=image_dir,
                                 img_name=img_name,
                                 colorkey=-1))
    return images


def get_speed(projectile_type: str) -> int:
    """
    Get the speed of the laser from the laser type

    :param projectile_type: The type of laser to load

    :return: The speed of the laser
    """

    if projectile_type == RED_LASER:
        return RED_LASER_SPEED
    elif projectile_type == BLUE_LASER:
        return BLUE_LASER_SPEED
    elif projectile_type == GREEN_LASER:
        return GREEN_LASER_SPEED
    elif projectile_type == ORANGE_LASER:
        return ORANGE_LASER_SPEED
    elif projectile_type == MISSILE:
        return MISSILE_SPEED
