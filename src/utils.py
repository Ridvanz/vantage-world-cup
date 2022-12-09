import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.font import Font
import settings as s
from pygame import Color
import json
import glob
import os


def load_jsons():
    
    # folder = os.path.join(os.path.dirname( __file__ ), '..', 'players')
    # filenames = glob.glob(folder + "\\*")

    dicts = []
    for file in ['players/samster.json', 'players/bob.json']:
        with open(file, 'r') as f:
            data = json.load(f)
            dicts.append(data)
    
    return dicts


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
  
def clip(x, l=0, u=1):
    return max(l, min(x, u))
