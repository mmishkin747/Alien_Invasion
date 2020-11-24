import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from  game_stats import GameStats
from button import Button


def run_game():
    """Инициализирует pygame, settings и обьект экрана."""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invansion")

    stats = GameStats(ai_settings)

    #Создание корабля.
    ship = Ship(ai_settings, screen)

    #Создаение группы для хранения пули
    bullets = Group()

    #Создание пришельца
    aliens = Group()

    #Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")

    #Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)


run_game()