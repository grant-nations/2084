from pygame.locals import *
import pygame

FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1100
PLAYER_Y = 950

SHIP_WIDTH = 48
SHIP_HEIGHT = 48

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load('background.png').convert()
player = pygame.image.load('sprites/spaceships/player.png').convert()
screen.blit(background, (0, 0))
screen.blit(player, ((SCREEN_WIDTH - SHIP_WIDTH)/2, PLAYER_Y))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.display.update()
    clock.tick(FPS)
