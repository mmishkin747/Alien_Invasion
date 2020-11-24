from pygame import display


class Settings():
    """Класс для хранения всех настроек игры Alien Invansion"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        #Парамаетры экрана.
        self.screen_width = display.Info().current_w
        self.screen_heigth = display.Info().current_h
        self.bg_collor = (170, 230, 230)
        #Настройки коробля
        self.ship_limit = 3
        #Параметры пули
        self.bullet_width = 300
        self.bullet_heigth = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 100
        # Настройки пришельцев
        self.fleet_drop_speed = 5

        #Темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изхменяющиеся в ходе игры"""
        self.ship_speed_factory = 1.5
        self.bullet_speed_factory = 3
        self.alien_speed_factor = 1

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1