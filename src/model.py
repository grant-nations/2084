from src.tesla import Model3, TESLA_WIDTH, TESLA_HEIGHT
from src.player import Player, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_LEFT, PLAYER_RIGHT
from src.projectile import Projectile, PROJECTILE_UP, PROJECTILE_DOWN
from utils.projectile_utils import RED_LASER, BLUE_LASER
from src.explosion import Explosion
from pygame.sprite import Group, GroupSingle, spritecollide
import pygame
from utils.main_utils import load_image

PADDING = 10


class Twenty84Game(object):
    def __init__(self,
                 screen_width: int,
                 screen_height: int,
                 fps: int,
                 data_dir: str):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.data_dir = data_dir

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.background = load_image(
            img_name='background.png', image_dir=data_dir, colorkey=-1)
        pygame.display.set_caption('2084')

        self.player_group = GroupSingle()
        self.player_lasers = Group()
        self.tesla_lasers = Group()
        self.model_3_teslas = Group()
        self.explosions = Group()

        self.player = self._make_player()
        self.player_group.add(self.player)

        self.wave_num = 1
        self.score = 0

        self.last_dir = None
        self.curr_dir = None
        self.delay_frames = fps  # 1 second
        self.respawn_frames = fps * 2  # 2 seconds
        self.player_lives = 3
        self.player_dead = False
        self.player_invincible = False

    def run(self):
        self._draw_initial()
        self._generate_wave()

        while self._player_has_lives():
            if self.player_invincible:
                self._decrement_invincibility()

            if self.player_dead:
                self._resurrect_player()

            self._handle_player_input()
            self._fire_lasers()
            self._clean_up_lasers()
            self._move_teslas()

            # Check for collisions
            if not self.player_invincible:
                self._handle_player_laser_collisions()

            self._handle_tesla_laser_collisions()
            self._handle_tesla_player_collisions()

            self._update_sprites()
            self._draw()

            self.clock.tick(self.fps)

        self._game_over_screen()

    def _game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.explosions.update()
            self.player_group.update()
            self.screen.blit(self.background, (0, 0))
            self.player_group.draw(self.screen)
            self.tesla_lasers.draw(self.screen)
            self.player_lasers.draw(self.screen)
            self.model_3_teslas.draw(self.screen)
            self.explosions.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def _handle_tesla_player_collisions(self):
        for tesla in self.model_3_teslas:
            if tesla.rect.colliderect(self.player.rect):
                self.explosions.add(Explosion(center=self.player.rect.center,
                                              data_dir=self.data_dir))
                self.explosions.add(Explosion(center=tesla.rect.center,
                                              data_dir=self.data_dir))
                tesla.mark_for_deletion()
                self.player_dead = True
                self.player_lives -= 1
                self.player.die()
                self.player_invincible = True
                self.respawn_frames = self.fps * 2

    def _handle_tesla_laser_collisions(self):
        for tesla in self.model_3_teslas:
            for laser in self.player_lasers:
                if tesla.rect.colliderect(laser.rect):
                    laser.mark_for_deletion()
                    tesla.mark_for_deletion()
                    self.explosions.add(Explosion(center=tesla.rect.center,
                                                  data_dir=self.data_dir))

    def _handle_player_laser_collisions(self):
        hit_list = spritecollide(self.player, self.tesla_lasers, False)
        if len(hit_list) > 0:
            self.explosions.add(Explosion(center=self.player.rect.center,
                                          data_dir=self.data_dir))
            self.player_dead = True
            self.player_lives -= 1
            self.player.die()
            self.player_invincible = True
            self.respawn_frames = self.fps * 2  # 2 seconds
            for laser in hit_list:
                laser.mark_for_deletion()

    def _move_teslas(self):
        # Handle model 3 movement
        reverse_direction = False
        for tesla in self.model_3_teslas:
            if tesla.rect.left < 10 or tesla.rect.right > self.screen_width - 10:
                reverse_direction = True
                break

        if reverse_direction:
            for tesla in self.model_3_teslas:
                tesla.reverse_direction()
                tesla.move_down()

        for tesla in self.model_3_teslas:
            if tesla.rect.bottom > self.screen_height:
                self.player_lives = 0
                break

    def _clean_up_lasers(self):
        # Delete lasers that are off the screen
        for laser in self.player_lasers:
            if laser.rect.y < 0 or laser.rect.y > self.screen_height + laser.rect.height:
                laser.mark_for_deletion()

        for laser in self.tesla_lasers:
            if laser.rect.y < 0 or laser.rect.y > self.screen_height + laser.rect.height:
                laser.mark_for_deletion()

    def _generate_wave(self):
        """Generate the next wave of enemies."""
        x_pos = 10
        y_pos = 10

        self.model_3_teslas.empty()

        # -3 to leave space for movement
        num_in_row = self.screen_width // (TESLA_WIDTH + PADDING) - 3

        # model s: fastest
        # start spawning at wave 2
        num_s = max((self.wave_num - 1), 0) * num_in_row

        # model 3: second fastest
        # start spawning at wave 1
        num_3 = self.wave_num * num_in_row

        for i in range(1, num_3 + 1):

            model_3 = Model3(x=x_pos,
                             y=y_pos,
                             data_dir=self.data_dir)
            self.model_3_teslas.add(model_3)

            if i % num_in_row == 0:
                x_pos = 10
                y_pos += TESLA_HEIGHT + 10
            else:
                x_pos += TESLA_WIDTH + 10

        # model x: second slowest
        # start spawning at wave 3
        num_x = min((self.wave_num - 2) * num_in_row, 0)

        # model y: slowest
        # start spawning at wave 4
        num_y = min((self.wave_num - 3) * num_in_row, 0)

    def _make_player(self):
        return Player(x=(self.screen_width - PLAYER_WIDTH)/2,
                      y=self.screen_height - PLAYER_HEIGHT - PADDING,
                      data_dir=self.data_dir)

    def _decrement_invincibility(self):
        if self.respawn_frames > 0:
            self.respawn_frames -= 1
        else:
            self.player_invincible = False

    def _resurrect_player(self):
        if self.delay_frames == 0:
            self.player_dead = False

            # make the player invincible for 2 seconds
            self.player_invincible = True

            # respawn the player
            player = self._make_player()
            self.player_group.add(player)
            self.player = player

            # reset the delay frames
            self.delay_frames = self.fps

            # reset the respawn frames
            self.respawn_frames = self.fps * 2  # 2 seconds
        else:
            self.delay_frames -= 1

    def _handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.last_dir = self.curr_dir
                    self.curr_dir = PLAYER_LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.last_dir = self.curr_dir
                    self.curr_dir = PLAYER_RIGHT
                elif event.key == pygame.K_SPACE:
                    self.player.shoot_laser()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.curr_dir = self.last_dir
                    self.last_dir = None
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.curr_dir = self.last_dir
                    self.last_dir = None

        keys_pressed = pygame.key.get_pressed()

        left_pressed = keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
        right_pressed = keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]
        both_pressed = left_pressed and right_pressed

        # Move the player
        if left_pressed and not both_pressed:
            self.player.move(PLAYER_LEFT, self.screen_width)

        if right_pressed and not both_pressed:
            self.player.move(PLAYER_RIGHT, self.screen_width)

        if both_pressed:
            self.player.move(self.curr_dir, self.screen_width)

    def _fire_lasers(self):
        if self.player.firing:
            self.player_lasers.add(Projectile(x=self.player.rect.centerx,
                                              y=self.player.rect.y,
                                              direction=PROJECTILE_UP,
                                              data_dir=self.data_dir,
                                              laser_type=RED_LASER))
            self.player.firing = False

        for tesla in self.model_3_teslas:
            if tesla.firing:
                self.tesla_lasers.add(Projectile(x=tesla.rect.centerx,
                                                 y=tesla.rect.bottom,
                                                 direction=PROJECTILE_DOWN,
                                                 data_dir=self.data_dir,
                                                 laser_type=BLUE_LASER))
                tesla.firing = False

    def _update_sprites(self):
        self.player_group.update()
        self.model_3_teslas.update()
        self.player_lasers.update()
        self.tesla_lasers.update()
        self.explosions.update()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player_group.draw(self.screen)
        self.tesla_lasers.draw(self.screen)
        self.player_lasers.draw(self.screen)
        self.model_3_teslas.draw(self.screen)
        self.explosions.draw(self.screen)
        pygame.display.flip()

    def _player_has_lives(self):
        return self.player_lives > 0

    def _draw_initial(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image,
                         (self.player.rect.x, self.player.rect.y))
        self.model_3_teslas.draw(self.screen)
        pygame.display.flip()
