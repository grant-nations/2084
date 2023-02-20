# Author: Grant Nations
# Date: 2/20/2023

import os
from src.twenty_84_game import Twenty84Game

FPS = 60
SCREEN_WIDTH = 590
SCREEN_HEIGHT = 700

if __name__ == '__main__':
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')

    game = Twenty84Game(data_dir=data_dir,
                        screen_height=SCREEN_HEIGHT,
                        screen_width=SCREEN_WIDTH,
                        fps=FPS)
    game.run()
