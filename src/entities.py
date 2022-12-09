import pygame
import random
import settings as s
import glob
from utils import clip

# class Ball(pygame.sprite.Sprite):
#       def __init__(self):
#         super().__init__() 
        
#         self.radius = 20
#         self.surf = pygame.Surface(size)
#         self.surf.fill(BLUE)

#         self.rect = self.surf.get_rect()
#         self.rect.center=(random.randint(40,s.SCREEN_WIDTH-40),0) 
 
#       def move(self):
#         self.rect.move_ip(0,10)
#         if (self.rect.bottom > 600):
#             self.rect.top = 0
#             self.rect.center = (random.randint(30, 370), 0)
 
#       def draw(self, surface):
#         surface.blit(self.surf, self.rect) 
 

class Player(pygame.sprite.Sprite):
    def __init__(self, ):
        super(Player, self).__init__()
        
        self.name = "Vantage AI"
        
        self.score = 0
        self.colors = (s.ORANGE, s.BLUE)

        self.power = 50
        self.accuracy = 50
        self.curve = 50 
        
        self.reach = 50
        self.speed = 50
        self.predict = 50
        
        self.max_points = 600
        
        self.shooter_radius = 40 + self.power/4
        self.keeper_radius = 40 + self.reach/4
        
    def set_attributes(self, player_dict):
        
        self.name = player_dict.get("name")
        self.colors = (player_dict.get("colors").get("primary"), player_dict.get("colors").get("secondary"))
                
        self.power = clip(player_dict.get("stats").get("shooter").get("power"), 0, 100)
        self.accuracy = clip(player_dict.get("stats").get("shooter").get("accuracy"), 0, 100)
        self.curve = clip(player_dict.get("stats").get("shooter").get("curve"), 0, 100)
        self.reach = clip(player_dict.get("stats").get("keeper").get("reach"), 0, 100)
        self.speed = clip(player_dict.get("stats").get("keeper").get("speed"), 0, 100)
        self.predict = clip(player_dict.get("stats").get("keeper").get("predict"), 0, 100)
        
        total_points = self.power+self.accuracy+self.curve+self.reach+self.speed+self.predict
        
        normalize = total_points/self.max_points
        
        self.power *= normalize
        self.accuracy *= normalize
        self.curve *= normalize
        self.reach *= normalize
        self.speed *= normalize
        self.predict *= normalize
        
        self.shooter_radius = 40 + self.power/4
        self.keeper_radius = 40 + self.reach/4
        
        
    def scored(self):
        self.score += 1
        
    def reset_score(self):
        self.score = 0
    
    def update(self):
        
        pass
    
    

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, s_x, s_y, size=s.ENEMY_SIZE, color=s.RED):
#         super(Enemy, self).__init__()
        
#         if s.SPRITES:
#             images = glob.glob("assets/images/enemies/*")
#             self.random_image = random.choice(images)
#             self.surf = pygame.image.load(self.random_image)
#             self.surf = pygame.transform.scale(self.surf, size)
#         else:
#             self.surf = pygame.Surface(size)
#             self.surf.fill(color)
            
#         self.rect = self.surf.get_rect()
#         self.bottom_border = s.WINDOW_HEIGHT

#         self.rect.left = s_x
#         self.s_x = s_x
#         self.s_y = s_y
        

#     def update(self, s_y):
        
#         self.rect.bottom = self.bottom_border - s.PLAYER_HEIGHT - (self.s_y - s_y)

#         if self.rect.bottom > self.bottom_border + s.ENEMY_SIZE[1]:
#             self.kill()
            