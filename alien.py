import pygame;
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__();
        self.screen = screen;
        self.settings  = settings;

        self.image = pygame.image.load('img/ufo_lvl2.1.png');
        self.rect = self.image.get_rect();

        self.rect.x = self.rect.width;
        self.rect.y = self.rect.height;

        self.x = float(self.rect.x);



    def check_edges(self):
        """Возвращает true если пришелец у края экрана"""
        screen_rect = self.screen.get_rect();
        if self.rect.right >= screen_rect.right:
            return True;
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Перемещение пришельцев"""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction);
        self.rect.x = self.x;

    def bitme(self):
        self.screen.blit(self.image, self.rect);