import pygame
import random
import settings as s
import glob

class Ball(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        
        self.radius = 20
        self.surf = pygame.Surface(size)
        self.surf.fill(BLUE)

        self.rect = self.surf.get_rect()
        self.rect.center=(random.randint(40,s.SCREEN_WIDTH-40),0) 
 
      def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
      def draw(self, surface):
        surface.blit(self.surf, self.rect) 
 


class Player(pygame.sprite.Sprite):
    def __init__(self, ):
        super(Player, self).__init__()
        
        # if s.SPRITES:
        #     self.surf = pygame.image.load("assets/images/car.png")
        #     self.surf = pygame.transform.scale(self.surf, size)
        # else:
        #     self.surf = pygame.Surface(size)
        #     self.surf.fill(color)
        self.score = 0
        self.radius = s.PLAYER_SIZE
        self.colors = (s.ORANGE, s.GREEN)

        self.power = 50
        self.accuracy = 50
        self.curve = 50 
        
        self.reach = 50
        self.speed = 50
        self.predict = 50
        
        
        
    def scored(self):
        self.score =+ 1
    
    def update(self):
        
        pass
    
    


class Enemy(pygame.sprite.Sprite):
    def __init__(self, s_x, s_y, size=s.ENEMY_SIZE, color=s.RED):
        super(Enemy, self).__init__()
        
        if s.SPRITES:
            images = glob.glob("assets/images/enemies/*")
            self.random_image = random.choice(images)
            self.surf = pygame.image.load(self.random_image)
            self.surf = pygame.transform.scale(self.surf, size)
        else:
            self.surf = pygame.Surface(size)
            self.surf.fill(color)
            
        self.rect = self.surf.get_rect()
        self.bottom_border = s.WINDOW_HEIGHT

        self.rect.left = s_x
        self.s_x = s_x
        self.s_y = s_y
        

    def update(self, s_y):
        
        self.rect.bottom = self.bottom_border - s.PLAYER_HEIGHT - (self.s_y - s_y)

        if self.rect.bottom > self.bottom_border + s.ENEMY_SIZE[1]:
            self.kill()
            