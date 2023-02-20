from utils.utils import load_image
from typing import List
from pygame import Surface


def get_explosion_images(data_dir: str) -> List[Surface]:
    """
    Get the image frames for explosion animation

    :param data_dir: The directory where the images are located

    :return: A list of images
    """

    images = []
    for i in range(1, 12):
        index = f'{i}' if i > 9 else f'0{i}'

        img_name = f'explosion-{index}.png'
        images.append(load_image(image_dir=data_dir,
                                 img_name=img_name,
                                 colorkey=-1))

    return images
