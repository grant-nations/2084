import pygame
import os

from pygame.sprite import Group
from src.player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
from utils.utils import LEFT, RIGHT

FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1100
PLAYER_INIT_Y = 950

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'img')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load('img/background.png').convert()
sprites = Group()

player = Player(x=(SCREEN_WIDTH - PLAYER_WIDTH)/2,
                y=PLAYER_INIT_Y,
                data_dir=data_dir)
sprites.add(player)

# initial draw
screen.blit(background, (0, 0))
sprites.draw(screen)

last_dir = None
curr_dir = None

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                last_dir = curr_dir
                curr_dir = LEFT
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                last_dir = curr_dir
                curr_dir = RIGHT
            elif event.key == pygame.K_SPACE:
                pass  # TODO
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                curr_dir = last_dir
                last_dir = None
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                curr_dir = last_dir
                last_dir = None
            elif event.key == pygame.K_SPACE:
                pass

    keys_pressed = pygame.key.get_pressed()

    left_pressed = keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
    right_pressed = keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]
    both_pressed = left_pressed and right_pressed

    if left_pressed and not both_pressed:
        player.move(LEFT)

    if right_pressed and not both_pressed:
        player.move(RIGHT)

    if both_pressed:
        player.move(curr_dir)

    if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP]:
        player.shoot_laser()

    sprites.update()  # TODO: write this method

    # Draw Everything
    screen.blit(background, (0, 0))
    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
