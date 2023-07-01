import sys
import time
import random

import pygame

from src.components.game_status import GameStatus
from src.components.hand import Hand
from src.components.hand_side import HandSide
from src.components.player import Player
from src.components.scoreboard import Scoreboard
from src.components.gift import Gift  # Добавлен импорт класса Gift
from src.global_state import GlobalState
from src.services.music_service import MusicService
from src.services.visualization_service import VisualizationService
from src.utils.tools import update_background_using_scroll, update_press_key, is_close_app_event
from src.config import Config

GlobalState.load_main_screen()
VisualizationService.load_main_game_displays()

scoreboard = Scoreboard()
gift_spawn_counter = 0

# Sprite Setup
P1 = Player()
H1 = Hand(HandSide.RIGHT)
H2 = Hand(HandSide.LEFT)
gift = None

# Sprite Groups
hands = pygame.sprite.Group()
hands.add(H1)
hands.add(H2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(H1)
all_sprites.add(H2)


def main_menu_phase():
    if gift is not None:
        gift.kill()

    scoreboard.reset_current_score()

    events = pygame.event.get()

    for event in events:
        if is_close_app_event(event):
            GlobalState.GAME_STATE = GameStatus.GAME_END
            return

        if event.type == pygame.KEYDOWN:
            GlobalState.GAME_STATE = GameStatus.GAMEPLAY

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)
    GlobalState.PRESS_Y = update_press_key(GlobalState.PRESS_Y)
    VisualizationService.draw_main_menu(GlobalState.SCREEN, scoreboard.get_max_score(), GlobalState.PRESS_Y)


def gameplay_phase():
    global gift_spawn_counter
    global gift

    events = pygame.event.get()

    for event in events:
        if is_close_app_event(event):
            game_over()
            return

    P1.update()

    H1.move(scoreboard, P1.player_position)
    H2.move(scoreboard, P1.player_position)

    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

    P1.draw(GlobalState.SCREEN)
    H1.draw(GlobalState.SCREEN)
    H2.draw(GlobalState.SCREEN)
    scoreboard.draw(GlobalState.SCREEN)

    if pygame.sprite.spritecollide(P1, hands, False, pygame.sprite.collide_mask):
        scoreboard.update_max_score()
        MusicService.play_slap_sound()
        time.sleep(0.5)
        game_over()

    if gift is None:
        if scoreboard._current_score >= gift_spawn_counter + 5:
            gift_spawn_counter = scoreboard._current_score
            spawn_gift()

    if gift is not None:
        if pygame.sprite.collide_rect(P1, gift):
            #gift_spawn_counter = int(scoreboard._current_score * 1.2) + 2
            #scoreboard._current_score = int(scoreboard._current_score * 1.2)
            gift_spawn_counter = scoreboard._current_score + 10
            scoreboard._current_score = scoreboard._current_score + 5
            MusicService.play_gift_bonus_sound()
            gift.kill()
            gift = None
        else:
            gift.draw(GlobalState.SCREEN)

def spawn_gift():
    global gift

    MusicService.play_gift_spawn_sound()

    x = random.randint(0, Config.WIDTH - Gift.WIDTH)
    y = right_y()

    gift = Gift(x, y)

def exit_game_phase():
    pygame.quit()
    sys.exit()

def right_y():
    y = 300
    while y < 100:
        y = random.randint(0, Config.HEIGHT - Gift.HEIGHT)
    return y

def game_over():
    global gift_spawn_counter

    P1.reset()
    H1.reset()
    H2.reset()
    gift_spawn_counter = 0
    GlobalState.GAME_STATE = GameStatus.MAIN_MENU
    time.sleep(0.5)
