import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scorebord:
    """Класс для вывода игровой информации"""

    def __init__(self, ai_settings, screen, stats):
        """Инициализирует атрибуты подсчета очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Настройки шрифта для вывода подсчета
        self.text_color = [30, 30, 30]
        self.black = [105, 105, 105]
        self.font = pygame.font.SysFont(None, size=48)

        # Подготовка изображения счета
        self.prep_score()
        self.prep_high_score()

        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """Преобразует текущий счет в изображение"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_collor)

        # Вывод счета в правом верхнейчасти экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Вывод текущий счет, рекорд и число оставшихся короблей"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Выод коробля
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Пеобразует рекордный счет в Графическое изображение"""
        high_score = int(round(self.stats.score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_collor)

        #Рекорды выравниваются по центру верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует уровунь в графическое изображение"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_collor)

        #Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ship(self):
        """сообщает количество оставшихся короблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10  + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
