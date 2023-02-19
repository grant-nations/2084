from utils.utils import load_image
from typing import List
from pygame import Surface


LASER_HEIGHT = LASER_WIDTH = 32

RED_LASER = 'red_laser'
RED_LASER_SPEED = 3
RED_LASER_IMAGES = ['red_laser_1.png',
                    'red_laser_2.png',
                    'red_laser_3.png']

BLUE_LASER = 'blue_laser'
BLUE_LASER_SPEED = 7
BLUE_LASER_IMAGES = ['blue_laser_1.png',
                     'blue_laser_2.png',
                     'blue_laser_3.png']

GREEN_LASER = 'green_laser'
GREEN_LASER_SPEED = 5
GREEN_LASER_IMAGES = ['green_laser_1.png',
                      'green_laser_2.png',
                      'green_laser_3.png']

ORANGE_LASER = 'orange_laser'
ORANGE_LASER_SPEED = 10
ORANGE_LASER_IMAGES = ['orange_laser_1.png',
                       'orange_laser_2.png',
                       'orange_laser_3.png']


def load_images(laser_type: str,
                image_dir: str) -> List[Surface]:
    """Load the images for the laser"""
    images = []

    if laser_type == RED_LASER:
        for img_name in RED_LASER_IMAGES:
            images.append(load_image(image_dir=image_dir,
                                     img_name=img_name,
                                     colorkey=-1))
    elif laser_type == BLUE_LASER:
        for img_name in BLUE_LASER_IMAGES:
            images.append(load_image(image_dir=image_dir,
                                     img_name=img_name,
                                     colorkey=-1))

    elif laser_type == GREEN_LASER:
        for img_name in GREEN_LASER_IMAGES:
            images.append(load_image(image_dir=image_dir,
                                     img_name=img_name,
                                     colorkey=-1))

    elif laser_type == ORANGE_LASER:
        for img_name in ORANGE_LASER_IMAGES:
            images.append(load_image(image_dir=image_dir,
                                     img_name=img_name,
                                     colorkey=-1))
    return images


def get_speed(laser_type: str):
    """Get the speed of the laser from the laser type"""

    if laser_type == RED_LASER:
        return RED_LASER_SPEED
    elif laser_type == BLUE_LASER:
        return BLUE_LASER_SPEED
    elif laser_type == GREEN_LASER:
        return GREEN_LASER_SPEED
    elif laser_type == ORANGE_LASER:
        return ORANGE_LASER_SPEED
