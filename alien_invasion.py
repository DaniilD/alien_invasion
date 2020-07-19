import sys;

import pygame;
from pygame.sprite import Group;

from settings import Settings;
from ship import Ship;
from alien import Alien;
import game_functions as gf;
from gamestat import GameStats;
from button import Button;
from scoreboard import Scoreboard;

def run_game():
    #инициализируем игру и создаем объект экрана
    pygame.init();
    st = Settings();
    bullets = Group();
    aliens = Group();
    
    screen = pygame.display.set_mode((st.screen_width, st.screen_height));
    pygame.display.set_caption("Alien Invasion");
    play_button = Button(st,screen,"Play");
    ship = Ship(st,screen);
    gf.create_fleet(st, screen, ship, aliens);
    stats = GameStats(st);
    sb = Scoreboard(st, screen, stats);
    
    #запуск основного цикла игры
    while True:
        #отслеживание событий клавиатуры и мыши
        gf.check_events(st,screen,ship, aliens, bullets, play_button, stats);
        
        ship.update();
        gf.update_bullets(st, screen, ship, aliens, bullets, stats, sb);
        gf.update_aliens(st, stats, screen, ship, aliens, bullets);
        gf.update_screen(st, screen, ship, aliens, bullets, play_button, stats, sb);


run_game();
