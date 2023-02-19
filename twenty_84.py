import pygame
import os

from pygame.sprite import Group, GroupSingle, spritecollide
from src.player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
from src.projectile import Projectile
from utils.main_utils import LEFT, RIGHT, UP, DOWN
from utils.projectile_utils import RED_LASER, BLUE_LASER
from src.tesla import Model3, ModelX, ModelY, ModelS
from utils.tesla_utils import TESLA_HEIGHT, TESLA_WIDTH
from src.explosion import Explosion

FPS = 60
SCREEN_WIDTH = 590
SCREEN_HEIGHT = 700
PLAYER_INIT_Y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10

# TODO: refactor this into a class, moving data_dir into the class


def generate_wave(data_dir: str,
                  wave_num: int,
                  model_3_teslas: Group,):
    """Generate the enemies for the given wave"""

    model_3_teslas.empty()

    num_in_row = SCREEN_WIDTH // (TESLA_WIDTH + 10) - 3

    # model s: fastest, least health
    # start spawning at wave 2. These are the only enemies that
    # can spawn in the row of enemies at the top of the screen
    num_s = max((wave_num - 1), 0)

    # model 3: second fastest, medium health
    x_pos = 10
    y_pos = 10

    num_3 = wave_num * num_in_row
    for i in range(1, num_3 + 1):

        model_3 = Model3(x=x_pos,
                         y=y_pos,
                         data_dir=data_dir)
        model_3_teslas.add(model_3)

        if i % num_in_row == 0:
            x_pos = 10
            y_pos += TESLA_HEIGHT + 10
        else:
            x_pos += TESLA_WIDTH + 10

    # model x: second slowest, second heighest health
    # max 20, start spawning at wave 3
    num_x = min((wave_num - 2) * num_in_row, 0)

    # model y: slowest, most health
    # max 20, start spawning at wave 4
    num_y = min((wave_num - 3) * num_in_row, 0)


if __name__ == '__main__':
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'img')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.image.load('img/background.png').convert()
    pygame.display.set_caption('2084')

    player_group = GroupSingle()
    player_lasers = Group()
    tesla_lasers = Group()
    model_3_teslas = Group()
    explosions = Group()

    player = Player(x=(SCREEN_WIDTH - PLAYER_WIDTH)/2,
                    y=PLAYER_INIT_Y,
                    data_dir=data_dir)
    player_group.add(player)

    # generate the first wave

    wave_num = 1
    generate_wave(data_dir=data_dir,
                  wave_num=wave_num,
                  model_3_teslas=model_3_teslas)

    # initial draw
    screen.blit(background, (0, 0))
    screen.blit(player.image, (player.rect.x, player.rect.y))
    model_3_teslas.draw(screen)
    pygame.display.flip()

    last_dir = None
    curr_dir = None

    player_lives = 3
    player_dead = False
    delay_frames = FPS  # 1 second
    respawn_frames = FPS * 2  # 2 seconds
    invincible = False

    # main loop
    while player_lives > 0:

        if invincible:
            if respawn_frames > 0:
                respawn_frames -= 1
            else:
                invincible = False

        if player_dead:
            if delay_frames == 0:
                player_dead = False
                invincible = True
                player = Player(x=(SCREEN_WIDTH - PLAYER_WIDTH)/2,
                                y=PLAYER_INIT_Y,
                                data_dir=data_dir)
                player_group.add(player)
                delay_frames = FPS
                respawn_frames = FPS * 2  # 2 seconds
            else:
                delay_frames -= 1

        # Get player input
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
                    player.shoot_laser()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    curr_dir = last_dir
                    last_dir = None
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    curr_dir = last_dir
                    last_dir = None

        keys_pressed = pygame.key.get_pressed()

        left_pressed = keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
        right_pressed = keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]
        both_pressed = left_pressed and right_pressed

        # Move the player
        if left_pressed and not both_pressed:
            player.move(LEFT, SCREEN_WIDTH)

        if right_pressed and not both_pressed:
            player.move(RIGHT, SCREEN_WIDTH)

        if both_pressed:
            player.move(curr_dir, SCREEN_WIDTH)

        # Shoot lasers
        if player.firing:
            player_lasers.add(Projectile(x=player.rect.centerx,
                                         y=player.rect.y,
                                         direction=UP,
                                         data_dir=data_dir,
                                         laser_type=RED_LASER))
            player.firing = False

        for tesla in model_3_teslas:
            if tesla.firing:
                tesla_lasers.add(Projectile(x=tesla.rect.centerx,
                                            y=tesla.rect.bottom,
                                            direction=DOWN,
                                            data_dir=data_dir,
                                            laser_type=BLUE_LASER))
                tesla.firing = False

        # Delete lasers that are off the screen
        for laser in player_lasers:
            if laser.rect.y < 0 or laser.rect.y > SCREEN_HEIGHT + laser.rect.height:
                laser.mark_for_deletion()

        for laser in tesla_lasers:
            if laser.rect.y < 0 or laser.rect.y > SCREEN_HEIGHT + laser.rect.height:
                laser.mark_for_deletion()

        # Handle model 3 movement
        reverse_direction = False
        for tesla in model_3_teslas:
            if tesla.rect.left < 10 or tesla.rect.right > SCREEN_WIDTH - 10:
                reverse_direction = True
                break

        if reverse_direction:
            for tesla in model_3_teslas:
                tesla.reverse_direction()
                tesla.move_down()

        # Check for collisions

        if not invincible:
            hit_list = spritecollide(player, tesla_lasers, False)
            if len(hit_list) > 0:
                explosions.add(Explosion(center=player.rect.center,
                                         data_dir=data_dir))
                player_dead = True
                player_lives -= 1
                player.die()
                invincible = True
                respawn_frames = FPS * 2  # 2 seconds
                for laser in hit_list:
                    laser.mark_for_deletion()

        for tesla in model_3_teslas:
            for laser in player_lasers:
                if tesla.rect.colliderect(laser.rect):
                    laser.mark_for_deletion()
                    tesla.mark_for_deletion()
                    explosions.add(Explosion(center=tesla.rect.center,
                                             data_dir=data_dir))

        # Update all sprites
        model_3_teslas.update()
        tesla_lasers.update()
        player_lasers.update()
        tesla_lasers.update()
        explosions.update()
        player_group.update()

        # Draw Everything
        screen.blit(background, (0, 0))

        player_group.draw(screen)
        tesla_lasers.draw(screen)
        player_lasers.draw(screen)
        model_3_teslas.draw(screen)
        explosions.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    # Game over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        explosions.update()
        player_group.update()

        screen.blit(background, (0, 0))

        player_group.draw(screen)
        tesla_lasers.draw(screen)
        player_lasers.draw(screen)
        model_3_teslas.draw(screen)
        explosions.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)
