"""
Author Paul Brace April 2024
Galaxians type space invaders game developed using PyGame
Most images copied from myripod-master
Music Goddess of Fate by Makai Symphony
"""

import pygame
pygame.init()
import random
import constants as const
import stars
# As an alternative field_stars gives a different star background
# import field_stars
from player import Player
from alien import Alien
from missile import Missile
from explosion import Explosion
from defence import Defence
from score_board import ScoreBoard
from sprite_list import SpriteList
import grids

screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption('Alien Attack')
clock = pygame.time.Clock()
running = True

player = Player()
aliens = SpriteList()
missiles = SpriteList()
bombs = SpriteList()
explosions = SpriteList()
defences = SpriteList()
score_board = ScoreBoard()
score_board.lives = 3
score_board.load_high_score()

music = pygame.mixer.Sound('sounds/AlienAttack.mp3')
music.set_volume(0.25)
game_over = pygame.mixer.Sound('sounds/GameOver.wav')

DEFENCE_GRAY = (82, 105, 130)
short_pause = 0
next_level_pause = 0

def create_defences():
    # Create defences
    defences.clear_all()
    for i in range(4):
        for j in range(3):
            defences.add(Defence(120 + i * 160 + j * 40, const.HEIGHT - player.height - 50))

def start_game(reset_defences):
    global short_pause
    """ Called at the beginning of each life """
    # Clear game objects
    aliens.clear_all()
    missiles.clear_all()
    bombs.clear_all()
    explosions.clear_all()
    # Create stars
    stars.initialize_stars()
    # or
    # field_stars.initialize_stars()
    if reset_defences:
        create_defences()
    # Create alien grid
    for y, row in enumerate(grids.grid_layouts[score_board.level % 10 - 1]):
        for x in range(0, len(row)):
            if row[x] == "x":
                aliens.add(
                    Alien(y + 1, x, "normal"))
    # for row in range(4):
    #     for col in range(8 - row * 2):
    #         aliens.add(
    #             Alien(row + 1, col + row, "normal"))
    # Do not move until player hits G
    Alien.moving = False
    # Set timer for cross flying alien
    Alien.crossing_alien_timer = random.randint(200, 500)
    short_pause = const.DELAY


start_game(True)

def clear_done_objects():
    aliens.clear_done()
    missiles.clear_done()
    bombs.clear_done()
    explosions.clear_done()
    defences.clear_done()

def update_game():
    global short_pause, next_level_pause
    # see if need to pause game for a few frames
    if short_pause > 0:
        short_pause -= 1
        if short_pause == 0:
            Alien.moving = True
        return
    if next_level_pause > 0:
        next_level_pause -= 1
        if next_level_pause == 0:
            score_board.score += 250
            score_board.level += 1
            # reset screen and increase the number of bombs the aliens drop and speed
            if Missile.bomb_interval > 20:
                Missile.bomb_interval -= 3
            if Missile.bomb_speed < 12:
                Missile.bomb_speed += 2
            if Alien.speed < 6:
                Alien.speed += 0.5
            player.reset()
            start_game(False)
            return

    if aliens.number() < 1 and next_level_pause == 0:
        # give bonus for clearing all aliens
        next_level_pause = const.DELAY

    if player.done:
        player.reset()
        # reset bomb speed
        Alien.speed = Alien.start_speed
        Missile.bomb_speed = Missile.start_bomb_speed
        Missile.bomb_interval = Missile.start_bomb_interval
        if score_board.lives < 1:
            score_board.game_state = const.GAME_OVER
            music.stop()
            game_over.play()
        else:
            start_game(False)
        return

    for explosion in explosions.list:
        explosion.update()

    if player.update() == "fire" and player.alive and player.timer <= 0:
        # True = space pressed
        # Player fires
        missile = Missile(player.x, player.y - 8, 'up')
        missile.bullet_sound()
        missiles.add(missile)
        player.timer = Player.RELOAD_TIME

    for bomb in bombs.list:
        bomb.update()
        if player.alive and bomb.collide_rect(player):
            player.hit()
            score_board.lives -= 1
            explosions.add(Explosion(player.x, player.y, 50, "red", 0.05))
            bomb.done = True
        else:
            for defence in defences.list:
                if bomb.collide_rect(defence):
                    defence.hit()
                    explosions.add(Explosion(defence.x, defence.y, 50, DEFENCE_GRAY, 0.05))
                    bomb.done = True
                    break

    for missile in missiles.list:
        missile.update()
        # Check if hit an alien
        for alien in aliens.list:
            if missile.collide_circle(alien):
                score_board.score += alien.hit()
                if alien.atype == "normal":
                    color = "aqua"
                else:
                    color = "orchid1"
                explosions.add(Explosion(alien.x, alien.y, 50, color, 0.05))
                missile.done = True
                break
        for bomb in bombs.list:
            if missile.collide_circle(bomb):
                explosions.add(Explosion(bomb.x, bomb.y, 50, "white", 0.05))
                missile.done = True
                bomb.done = True
                score_board.score += 20
                break

    # drop bombs and set aliens flying
    if Alien.moving and len(aliens.list) > 0:
        # create a crossing alien if timer expired
        Alien.crossing_alien_timer -= 1
        if Alien.crossing_alien_timer < 0:
            if random.random() > 0.5:
                aliens.add(Alien(0, 0, "cright"))
            else:
                aliens.add(Alien(0, 0, "cleft"))
            Alien.crossing_alien_timer = random.randint(200, 500)
        # drop a bomb from a random alien every bomb_interval
        Missile.bomb_timer -= 1
        if (Missile.bomb_timer < 1):
            dropping = aliens.list[random.randint(0, len(aliens.list) - 1)]
            Missile.bomb_timer = Missile.bomb_interval
            # drop bomb from chosen alien
            bombs.add(Missile(dropping.x,
                                 dropping.y + 40, 'down'))
        # set a random alien to fly every fly interval
        Alien.fly_timer -= 1
        if Alien.fly_timer < 1:
            fly = random.randint(0, len(aliens. list) - 1)
            Alien.fly_timer = Alien.fly_interval
            aliens.list[fly].start_flying(player.x, player.y)
        for alien in aliens.list:
            alien.update()
            if alien.atype == "normal" or alien.atype == "flying":
                # have we collided with a bolder
                for defence in defences.list:
                    if defence and not defence.exploding and defence.collide_circle(alien):
                        # record hit
                        defence.hit()
                        explosions.add(Explosion(defence.x, defence.y, 50, "dimgray", 0.05))
                        alien.done = True
                if player.alive and alien.collide_circle(player):
                    alien.done = True
                    explosions.add(Explosion(player.x, player.y, 50, "red", 0.05))
                    player.hit()
                    score_board.lives -= 1

    for defence in defences.list:
        defence.update()

def draw_starfield():
    screen.fill("black")
    stars.move_stars(screen)
    # or
    # field_stars.move_stars(screen)

def draw_game_screen():
    # fill the screen with a color to wipe away anything from last frame
    draw_starfield()
    player.draw(screen)
    aliens.draw(screen)
    missiles.draw(screen)
    bombs.draw(screen)
    defences.draw(screen)
    explosions.draw(screen)
    score_board.draw(screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X so end game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clear_done_objects()
    if score_board.game_state == const.INPLAY:
        update_game()
        draw_game_screen()
    elif score_board.game_state == const.GAME_OVER:
        draw_starfield()
        start, play = score_board.draw_game_over(screen)
        if start == "start":
            score_board.score = 0
            score_board.level = 1
            score_board.lives = 3
            Alien.speed = Alien.start_speed
            Missile.bomb_speed = Missile.start_bomb_speed
            Missile.bomb_interval = Missile.start_bomb_interval
            score_board.game_state = const.INPLAY
            short_pause = const.DELAY
            if play == "music":
                music.play(-1)
            start_game(True)
    else:
        draw_starfield()
        start, play = score_board.draw_game_instructions(screen)
        if  start == "start":
            score_board.game_state = const.INPLAY
            if play == "music":
                music.play(-1)
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()