from src.tesla import Proto3, ProtoS, ProtoX, ProtoY, TESLA_WIDTH, TESLA_HEIGHT, LEFT, RIGHT
from src.player import Player, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_LEFT, PLAYER_RIGHT, PLAYER_VERTICAL
from src.projectile import Projectile, PROJECTILE_UP
from utils.projectile_utils import MISSILE, ORANGE_LASER
from src.explosion import Explosion
from pygame.sprite import Group, spritecollide, spritecollideany
import pygame
from utils.utils import load_image, load_font


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

        self.player_group = Group()
        self.player_lasers = Group()
        self.tesla_projectiles = Group()
        self.proto_s_teslas = Group()
        self.proto_3_teslas = Group()
        self.proto_x_teslas = Group()
        self.proto_y_teslas = Group()
        self.enemies_to_draw = Group()
        self.enemy_thrusters = Group()
        self.explosions = Group()

        self.wave_num = 0
        self.wave_cooldown = 0
        self.in_wave = False
        self.score = 0

        self.last_dir = None
        self.curr_dir = None
        self.delay_frames = fps  # 1 second
        self.respawn_frames = fps * 2  # 2 seconds
        self.player_lives = 3
        self.player_dead = False
        self.player_invincible = False

        self.banner_height = 30
        self.padding = 10
        self.font_color = (255, 255, 255)
        self.font = load_font(font_dir=data_dir,
                              font_name='upheavtt.ttf',
                              size=24)

        self.player = self._make_player()
        self.player_group.add(self.player)
        self.player_group.add(self.player.thruster)
        self.paused = False

    def run(self):

        playing = True
        while playing:
            self._draw_start_screen()
            self._draw_initial()

            while self._player_has_lives():

                if self.paused:
                    self._draw_paused_screen()
                    self.paused = False

                if self.player_invincible:
                    self._decrement_invincibility()

                if self.player_dead:
                    self._resurrect_player()

                if self.in_wave:
                    if self.wave_cooldown > 0:
                        self.wave_cooldown -= 1
                    else:
                        self._update_wave()
                else:
                    self._start_wave()

                self._handle_player_input()
                self._fire_lasers()
                self._clean_up_lasers()
                self._check_tesla_at_bottom()
                self._reverse_proto_3_group()
                self._reverse_solo_teslas()

                # Check for collisions
                if not self.player_invincible:
                    self._handle_player_laser_collisions()

                self._handle_tesla_laser_collisions()
                self._handle_tesla_player_collisions()
                self._handle_missile_laser_collisions()

                self._update_sprites()
                self._draw()

                self.clock.tick(self.fps)

            playing = self._draw_game_over()

    def _game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.explosions.update()
            self.player_group.update()
            self.screen.blit(self.background, (0, 0))
            self.player_group.draw(self.screen)
            self.tesla_projectiles.draw(self.screen)
            self.player_lasers.draw(self.screen)
            self.enemies_to_draw.draw(self.screen)
            self.enemy_thrusters.draw(self.screen)
            self.explosions.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def _handle_tesla_player_collisions(self):
        for tesla in self.enemies_to_draw:
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
        for tesla in self.enemies_to_draw:
            for laser in self.player_lasers:
                if tesla.rect.colliderect(laser.rect):
                    laser.mark_for_deletion()
                    tesla.mark_for_deletion()
                    self.score += tesla.points
                    self.explosions.add(Explosion(center=tesla.rect.center,
                                                  data_dir=self.data_dir))

    def _handle_player_laser_collisions(self):
        hit_list = spritecollide(self.player, self.tesla_projectiles, False)
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

    def _handle_missile_laser_collisions(self):
        for proj in self.tesla_projectiles:
            if proj.projectile_type == MISSILE:
                for laser in self.player_lasers:
                    if proj.rect.colliderect(laser.rect):
                        laser.mark_for_deletion()
                        proj.mark_for_deletion()
                        self.explosions.add(Explosion(center=proj.rect.center,
                                                      data_dir=self.data_dir))

    def _check_tesla_at_bottom(self):
        for tesla in self.enemies_to_draw:
            if tesla.rect.bottom > self.screen_height:
                self.player_lives = 0
                return

    def _reverse_proto_3_group(self):
        reverse_direction = False
        for tesla in self.enemies_to_draw:
            # check if we need to reverse the direction of the
            # group of proto 3 teslas
            if type(tesla) is Proto3:
                if tesla.rect.left < self.padding or tesla.rect.right > self.screen_width - self.padding:
                    reverse_direction = True
                    break

        if reverse_direction:
            for tesla in self.enemies_to_draw:
                if type(tesla) is Proto3:
                    tesla.reverse_direction()
                    tesla.move_down()

    def _reverse_solo_teslas(self):
        for tesla in self.enemies_to_draw:
            if type(tesla) is not Proto3:
                if tesla.rect.left < self.padding or tesla.rect.right > self.screen_width - self.padding:
                    tesla.reverse_direction()

    def _clean_up_lasers(self):
        # Delete lasers that are off the screen
        for laser in self.player_lasers:
            if laser.rect.y < 0 or laser.rect.y > self.screen_height + laser.rect.height:
                laser.mark_for_deletion()

        for laser in self.tesla_projectiles:
            if laser.rect.y < 0 or laser.rect.y > self.screen_height + laser.rect.height:
                laser.mark_for_deletion()

    def _start_wave(self):
        self.wave_num += 1
        self.in_wave = True
        self.wave_cooldown = self.fps * 2  # 2 seconds

        self.proto_s_teslas.empty()
        self.proto_3_teslas.empty()
        self.proto_x_teslas.empty()
        self.proto_y_teslas.empty()
        self.enemies_to_draw.empty()
        self.enemy_thrusters.empty()

        # -3 to leave space for movement
        num_in_row = self.screen_width // (TESLA_WIDTH + self.padding) - 3

        # proto s: fastest
        # start spawning at wave 2
        # spawn a new proto 2 every 2 waves
        num_s = self.wave_num // 2

        x_pos = self.padding
        y_pos = self.padding + self.banner_height

        for i in range(1, num_s + 1):

            if i % 2 == 0:
                x_pos = self.screen_width - TESLA_WIDTH - self.padding
            else:
                x_pos = self.padding

            direction = LEFT if i % 2 == 0 else RIGHT

            proto_s = ProtoS(x=x_pos,
                             y=y_pos,
                             data_dir=self.data_dir,
                             move_direction=direction
                             )
            self.proto_s_teslas.add(proto_s)

        # proto 3: second fastest
        # start spawning at wave 1
        # spawn a new proto 3 row on every odd wave
        num_3 = min(5, (self.wave_num % 2) + (self.wave_num // 2)) * num_in_row
        # max 5 rows of proto 3 teslas

        x_pos = self.padding
        y_pos = self.padding + self.banner_height

        for i in range(1, num_3 + 1):

            proto_3 = Proto3(x=x_pos,
                             y=y_pos,
                             data_dir=self.data_dir)
            self.proto_3_teslas.add(proto_3)

            if i % num_in_row == 0:
                x_pos = 10
                y_pos += proto_3.rect.height + self.padding
            else:
                x_pos += proto_3.rect.width + self.padding

        # proto y: sporratic motion
        # start spawning at wave 4
        num_y = self.wave_num // 4

        x_pos = self.screen_width // 2 - TESLA_WIDTH // 2
        y_pos = self.padding + self.banner_height

        for i in range(1, num_y + 1):

            proto_y = ProtoY(x=x_pos,
                             y=y_pos,
                             data_dir=self.data_dir)
            self.proto_y_teslas.add(proto_y)

        # proto x: carpet bomb
        # start spawning at wave 5
        num_x = self.wave_num // 5

        x_pos = self.screen_width // 2 - TESLA_WIDTH // 2
        y_pos = self.padding + self.banner_height

        for i in range(1, num_x + 1):

            proto_x = ProtoX(x=x_pos,
                             y=y_pos,
                             data_dir=self.data_dir)
            self.proto_x_teslas.add(proto_x)

    def _update_wave(self):
        """Update the wave of enemies."""

        # if there are no more enemies to spawn and no enemies on the screen
        # and all enemies have been destroyed, then the wave is over
        if (len(self.proto_s_teslas) == 0 and len(self.proto_3_teslas) == 0 and
            len(self.proto_x_teslas) == 0 and len(self.proto_y_teslas) == 0 and
                len(self.enemies_to_draw) == 0):
            self.in_wave = False
            return

        can_spawn_proto_s = True
        for tesla in self.enemies_to_draw.sprites():

            if spritecollideany(tesla,
                                self.proto_s_teslas,
                                collided=lambda s1, s2: (s1.rect.top - self.padding) <= s2.rect.bottom):
                can_spawn_proto_s = False
                break

            if spritecollideany(tesla, self.explosions):
                can_spawn_proto_s = False
                break

        if can_spawn_proto_s and len(self.proto_s_teslas.sprites()) > 0:
            # remove from proto s teslas
            tesla = self.proto_s_teslas.sprites()[0]
            self.proto_s_teslas.remove(tesla)
            self.enemies_to_draw.add(tesla)  # add to enemies to draw
            self.enemy_thrusters.add(tesla.thruster)
            return

        can_spawn_proto_3 = True
        for tesla in self.enemies_to_draw.sprites():

            if spritecollideany(tesla,
                                self.proto_3_teslas,
                                collided=lambda s1, s2: (s1.rect.top - self.padding) <= s2.rect.bottom):
                can_spawn_proto_3 = False
                break

            if spritecollideany(tesla, self.explosions):
                can_spawn_proto_3 = False
                break

        if can_spawn_proto_3:
            for tesla in self.proto_3_teslas.sprites():
                self.proto_3_teslas.remove(tesla)
                self.enemies_to_draw.add(tesla)
                self.enemy_thrusters.add(tesla.thruster)

        can_spawn_proto_y = True
        for tesla in self.enemies_to_draw.sprites():

            if spritecollideany(tesla,
                                self.proto_y_teslas,
                                collided=lambda s1, s2: (s1.rect.top - self.padding) <= s2.rect.bottom):
                can_spawn_proto_y = False
                break

            if spritecollideany(tesla, self.explosions):
                can_spawn_proto_y = False
                break

        if can_spawn_proto_y and len(self.proto_y_teslas.sprites()) > 0:
            tesla = self.proto_y_teslas.sprites()[0]
            self.proto_y_teslas.remove(tesla)
            self.enemies_to_draw.add(tesla)
            self.enemy_thrusters.add(tesla.thruster)

        can_spawn_proto_x = len(self.proto_s_teslas) == 0 and len(
            self.proto_3_teslas) == 0 and len(self.proto_y_teslas) == 0

        if can_spawn_proto_x:
            for tesla in self.enemies_to_draw.sprites():

                if spritecollideany(tesla,
                                    self.proto_x_teslas,
                                    collided=lambda s1, s2: (s1.rect.top - self.padding) <= s2.rect.bottom):
                    can_spawn_proto_x = False
                    break

                if spritecollideany(tesla, self.explosions):
                    can_spawn_proto_x = False
                    break

        if can_spawn_proto_x and len(self.proto_x_teslas.sprites()) > 0:
            tesla = self.proto_x_teslas.sprites()[0]
            self.proto_x_teslas.remove(tesla)
            self.enemies_to_draw.add(tesla)
            self.enemy_thrusters.add(tesla.thruster)

    def _make_player(self):
        return Player(x=(self.screen_width - PLAYER_WIDTH)/2,
                      y=self.screen_height - PLAYER_HEIGHT - 3 * self.padding,
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
            self.player_group.add(player.thruster)
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
                elif event.key == pygame.K_ESCAPE:
                    self.paused = True
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
            self.player.set_direction(PLAYER_LEFT)
        elif right_pressed and not both_pressed:
            self.player.move(PLAYER_RIGHT, self.screen_width)
            self.player.set_direction(PLAYER_RIGHT)
        elif both_pressed:
            self.player.move(self.curr_dir, self.screen_width)
            self.player.set_direction(self.curr_dir)
        else:
            self.player.set_direction(PLAYER_VERTICAL)

    def _fire_lasers(self):
        if self.player.firing and not self.player_dead:
            self.player_lasers.add(Projectile(centerx=self.player.rect.centerx,
                                              y=self.player.rect.y,
                                              direction=PROJECTILE_UP,
                                              data_dir=self.data_dir,
                                              projectile_type=ORANGE_LASER))
            self.player.firing = False

        for tesla in self.enemies_to_draw:
            if tesla.firing:
                self.tesla_projectiles.add(
                    tesla.get_laser(data_dir=self.data_dir))
                tesla.firing = False

    def _update_sprites(self):
        self.player_group.update()
        self.enemies_to_draw.update()
        self.player_lasers.update()
        self.tesla_projectiles.update()
        self.explosions.update()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player_group.draw(self.screen)
        self.tesla_projectiles.draw(self.screen)
        self.player_lasers.draw(self.screen)
        self.enemies_to_draw.draw(self.screen)
        self.enemy_thrusters.draw(self.screen)
        self.explosions.draw(self.screen)
        self._draw_banner()
        pygame.display.flip()

    def _player_has_lives(self):
        return self.player_lives > 0

    def _draw_initial(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image,
                         (self.player.rect.x, self.player.rect.y))
        self.enemies_to_draw.draw(self.screen)
        pygame.display.flip()

    def _draw_banner(self):
        score_text = self.font.render(
            f'SCORE: {self.score}', True, self.font_color)

        lives_text = self.font.render(
            f'LIVES: {self.player_lives}', True, self.font_color)

        round_text = self.font.render(
            f'ROUND: {self.wave_num}', True, self.font_color)

        self.screen.blit(score_text, (self.padding, self.padding))
        self.screen.blit(lives_text, (self.screen_width -
                         lives_text.get_width() - self.padding, self.padding))
        self.screen.blit(round_text, ((self.screen_width -
                                       round_text.get_width())/2, self.padding))

    def _draw_game_over(self):

        play_again = False
        while not play_again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play_again = True

            self.explosions.update()
            self.player_group.update()
            self.screen.blit(self.background, (0, 0))
            self.player_group.draw(self.screen)
            self.tesla_projectiles.draw(self.screen)
            self.player_lasers.draw(self.screen)
            self.enemies_to_draw.draw(self.screen)
            self.enemy_thrusters.draw(self.screen)
            self.explosions.draw(self.screen)
            self._draw_banner()

            game_over_text = self.font.render(
                f'GAME OVER', True, self.font_color)
            self.screen.blit(game_over_text, ((self.screen_width -
                                               game_over_text.get_width())/2, (self.screen_height -
                                                                               game_over_text.get_height())/2))
            play_again_text = self.font.render(
                f'PRESS SPACE TO RETURN TO START', True, self.font_color)
            self.screen.blit(play_again_text, ((self.screen_width -
                                                play_again_text.get_width())/2, (self.screen_height -
                                                                                 play_again_text.get_height())/2 + 50))
            pygame.display.flip()

        return play_again

    def _draw_paused_screen(self):

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        exit()

            self.screen.blit(self.background, (0, 0))
            self.player_group.draw(self.screen)
            self.tesla_projectiles.draw(self.screen)
            self.player_lasers.draw(self.screen)
            self.enemies_to_draw.draw(self.screen)
            self.enemy_thrusters.draw(self.screen)
            self.explosions.draw(self.screen)
            self._draw_banner()

            pause_text = self.font.render(
                f'PAUSED', True, self.font_color)
            self.screen.blit(pause_text, ((self.screen_width -
                                           pause_text.get_width())/2, (self.screen_height -
                                                                       pause_text.get_height())/2))
            continue_text = self.font.render(
                f'PRESS SPACE TO CONTINUE', True, self.font_color)
            self.screen.blit(continue_text, ((self.screen_width -
                                              continue_text.get_width())/2, (self.screen_height -
                                                                             continue_text.get_height())/2 + 50))

            quit_text = self.font.render(
                f'PRESS ESC TO QUIT', True, self.font_color)
            self.screen.blit(quit_text, ((self.screen_width -
                                          quit_text.get_width())/2, (self.screen_height -
                                                                     quit_text.get_height())/2 + 100))

            pygame.display.flip()

    def _draw_start_screen(self):

        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True
            self.screen.blit(self.background, (0, 0))

            title_text = self.font.render(
                f'2084', True, self.font_color)
            self.screen.blit(title_text, ((self.screen_width -
                                           title_text.get_width())/2, (self.screen_height - title_text.get_height())/2))

            start_text = self.font.render(
                f'PRESS SPACE TO START', True, self.font_color)
            self.screen.blit(start_text, ((self.screen_width -
                                           start_text.get_width())/2, (self.screen_height -
                                                                       start_text.get_height())/2 + 50))
            pygame.display.flip()
