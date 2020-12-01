import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scorebord import Scorebord


def run_game():
    """Инициализирует pygame, settings и обьект экрана."""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invansion")

    # создание экземпляров GameStats и Scorebord
    stats = GameStats(ai_settings)
    sb = Scorebord(ai_settings, screen, stats)

    # Создание корабля.
    ship = Ship(ai_settings, screen)

    # Создаение группы для хранения пули
    bullets = Group()

    # Создание пришельца
    aliens = Group()

    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")

    # Запуск основного цикла игры
    while True:
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)



run_game()
