import pygame;

class Ship():
    
    def __init__(self, settings, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = screen;

        #Загрузка изображения корабля и получение прямоугольника
        self.image = pygame.image.load("img/Ship.png");
        self.rect = self.image.get_rect();
        self.screen_rect = screen.get_rect();
        #Каждый новый корабль появляется у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx;
        self.rect.bottom = self.screen_rect.bottom;

        self.moving_right = False;
        self.moving_left = False;

        self.settings = settings;
        self.center = float(self.rect.centerx);

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center +=self.settings.ship_speed;
        elif self.moving_left and self.rect.left > 0:
            self.center -=self.settings.ship_speed;

        self.rect.centerx = self.center;

    def bitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect);


    def center_ship(self):
        self.center = self.screen_rect.centerx;