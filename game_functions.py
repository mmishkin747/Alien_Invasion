import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        #Переместить корабыль вправо
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Обрабатывает нажатие клавиш и собития мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран."""
    #При каждом проходе цикла переррисовыется экран
    screen.fill(ai_settings.bg_collor)
    #Все пули выводятся позади изображения коробля и пришельцев
    for bullet in bullets:
        bullet.draw_bullet()

    # Кнопка Play Отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    ship.blitme()
    aliens.draw(screen)

    #Отображение последнего прорисованного экрана.
    pygame.display.flip()



def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Обновление позиции пули и уничтожает старые пули"""
    #Обновляет позиций пуль
    bullets.update()
    #Удаление пуль, вышедших за экран
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Проверка попадания в пришельца

    check_bullet_alien_collision(ai_settings, ship, bullets, screen, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут"""
    #Создание новой пули и включение ее в группу bullets
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряд"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return  number_alien_x

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряд"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    #Создание пришельцев и вычисление количества пришельцев в ряд
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)


    #Создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Создает пришельца и размещает его в ряду
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_heigth, alien_heigth):
    """Определяет количество рядов помещающихся на экране"""
    available_spase_y = (ai_settings.screen_heigth - (3 * alien_heigth) - ship_heigth)
    number_rows = int(available_spase_y / (2 * alien_heigth))
    return number_rows

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет достииг ли флот края экрана
    после чего обновляет позицию всех пришельцев во флоте
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверки коллизии "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # Проверка пришельцев, добравшихся до нижнего края экрана
    check_alien_buttom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collision(ai_settings, ship, bullets, screen, aliens):
    """Обработка колизии пуль с пришельцами"""
    #Удаление пуль и пришельцев участвующих в колизиях
    collosions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание флота
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обрабатыет столкновение коробля с пришельцем"""
    if stats.ships_left > 0:
        #Уменьшение ships_left
        stats.ships_left -= 1
        #Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()
        #Создание нового флота и размещение коробля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_buttom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет добралились ли пришельцы нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Происходит тоже что и при столкновении с короблем
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)
        #Сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True
        # Очищает список ппришельцев и пуль
        aliens.empty()
        bullets.empty()
        #Создание нового флота и размещение коробля по центру
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
