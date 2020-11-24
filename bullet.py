import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управление пули выпущенными кораблем"""
    def __init__(self, ai_setting, screen, ship):
        """Создает обьект пули в текущей позиции коробля"""
        super(Bullet, self).__init__()
        self.screen = screen

        #Создает пули в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_heigth)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Позиции пули хранятся в вещетвенном формате
        self.y = float(self.rect.y)

        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factory

    def update(self):
        """Перемещает пулю вверх по экрану"""
        #Обнрвление позиции пули в вещественном формате
        self.y -= self.speed_factor
        #Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод пули на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)