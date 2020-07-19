import sys;
import pygame;

from bullet import Bullet;
from alien import Alien;
from time import sleep;

def check_events(st,screen,ship, aliens, bullets, play_button, stats):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit();
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, st, ship, screen, bullets);
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship);
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos();
            check_play_button(st, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y);

def check_play_button(st, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y);
    if button_clicked and not stats.game_active:
        st.initialize_dynamic_settings();
        pygame.mouse.set_visible(False);
        stats.rest_stats();
        stats.game_active = True;
        aliens.empty();
        bullets.empty();

        create_fleet(st, screen, ship, aliens);
        ship.center_ship();

def update_screen(st, screen, ship, aliens, bullets, play_button, stats, sb):
    """Обновляет изображение на экране"""
    screen.fill(st.bg_color);
    for bullet in bullets.sprites():
        bullet.draw_bullet();
    ship.bitme();

    aliens.draw(screen);
    if not stats.game_active:
        play_button.draw_button();

    sb.show_score();

    pygame.display.flip();

def check_keydown_events(event, st, ship, screen, bullets):
    if event.key == pygame.K_RIGHT:
        #Переместить корабль вправо.
        ship.moving_right = True;
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True;
    elif event.key == pygame.K_SPACE:
    	fire_bullet(st, screen, ship, bullets);
    elif event.key == pygame.K_q:
        sys.exit();

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False;
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False;

def update_bullets(st, screen, ship, aliens, bullets, stats, sb):
    bullets.update();
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True);
    if collision:
        stats.score += st.alien_points;
        sb.prep_score();

    if len(aliens) == 0:
        bullets.empty();
        st.increase_speed();
        create_fleet(st, screen, ship, aliens);

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
           bullets.remove(bullet);
   # print(len(bullets));

def check_fleet_edges(st, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(st, aliens);
            break;


def change_fleet_direction(st, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += st.fleet_drop_speed;

    st.fleet_direction *= -1;

def update_aliens(st, stats, screen, ship, aliens, bullets):
    check_fleet_edges(st, aliens);
    aliens.update();
    check_aliens_bottom(st, stats, screen, ship, aliens, bullets);
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(st, stats, screen, ship, aliens, bullets);

def fire_bullet(st, screen, ship, bullets):
    if len(bullets) < st.bullet_allowed:
        new_bullet = Bullet(st,screen,ship);
        bullets.add(new_bullet);

def create_fleet(st, screen, ship, aliens):
    """Cоздание флота пришельцев"""
    alien = Alien(st, screen);
    alien_width = alien.rect.width;
    number_aliens_x = get_number_aliens_x(st, alien_width);
    number_rows = get_number_rows(st, ship.rect.height, alien.rect.height);

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Создание пришельца и размещение его в ряду
            create_alien(st, screen, aliens, alien_number, row_number);


def get_number_aliens_x(st, alien_width):
    """Вычисление кол-во пришельцев"""
    available_space_x = st.screen_width - 2 * alien_width;
    number_aliens_x = int(available_space_x / (2*alien_width));
    return number_aliens_x;

def create_alien(st, screen, aliens, alien_number, row_number):
    alien = Alien(st,screen);
    alien_width = alien.rect.width;
    alien.x = alien_width + 2*alien_width * alien_number;
    alien.rect.x = alien.x;
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number;
    aliens.add(alien);

def get_number_rows(st, ship_height, alien_height):
    """Определяем кол-во рядов помещающихся на экране"""
    available_space_y = (st.screen_height - (3*alien_height) - ship_height);
    number_rows = int(available_space_y / (2 * alien_height));
    return number_rows;


def ship_hit(st, stats, screen, ship, aliens, bullets):
    
    if stats.ships_left > 0:
        stats.ships_left -=1;

        aliens.empty();
        bullets.empty();

        create_fleet(st, screen, ship, aliens);
        ship.center_ship();

        sleep(0.5);
    else:
        stats.game_active = False;
        pygame.mouse.set_visible(True);

def check_aliens_bottom(st, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect();
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(st, stats, screen, ship, aliens, bullets);
            break;