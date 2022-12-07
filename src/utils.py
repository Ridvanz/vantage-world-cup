import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.font import Font
import settings as s
from pygame import Color

def try_quit(e):
    if e.type == QUIT or\
      (e.type == KEYDOWN and\
       e.key == K_ESCAPE):
        pygame.quit()
        sys.exit()


def HSV(h=360, s=100, v=100, a=100):
    color = Color(0)      
    color.hsva = (h,s,v,a)
    
    return color