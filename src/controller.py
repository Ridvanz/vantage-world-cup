import pygame
import settings as s
import scene
from sound import SoundManager
from tournament import TournamentSystem
from utils import load_jsons
import sys
import random
class GameController:

    def __init__(self):
        
        pygame.init()
        self.display = self._get_display()
        self.clock = self._get_clock()
        self.sceneManager = self._get_SceneManager()
        self.soundManager = SoundManager()
        self.tournamentSystem = TournamentSystem(self.sceneManager)
        # self.event_handler = EventHandler()
        self.running = True
        self.setup_tournement()
        
    def _get_display(self):
        if s.RENDER:
            display = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
            pygame.display.set_caption("Game")
        else:
            display = None
        
        return display

    def _get_clock(self):
        clock = pygame.time.Clock()
        return clock
    
    def _get_SceneManager(self):
        sceneManager = scene.SceneManager(self.display)
        intro = scene.IntroScene()
        sceneManager.push(intro)
        
        return sceneManager

    def setup_tournement(self):
        self.tournamentSystem.get_players()

    def run(self, tournament = True):
        
        if tournament:
            self.setup_tournement()
            players = self.tournamentSystem.players[:2]
            random.shuffle(players)
            P1, P2 = players
            
            self.sceneManager.P1 = P1
            self.sceneManager.P2 = P2
            
        while self.running:
            load_jsons()
            self.sceneManager.input()
            self.sceneManager.update()
            self.sceneManager.render()
            self.handle_events()
            self.tick_clock()
            # self.check_env_changes()

    def tick_clock(self):
        self.clock.tick(s.FPS)

    def handle_events(self):
        # self.event_handler.handle_events(self.state.actor)
        # print(len(pygame.event.get()))
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT or\
        #         (event.type == pygame.KEYDOWN and\
        #         event.key == pygame.K_ESCAPE):
        #         self.running = False
                
        #         pygame.quit()
        #         sys.exit()    
        pass
    # def try_quit(e):
    #     if e.type == QUIT or\
    #     (e.type == KEYDOWN and\
    #     e.key == K_ESCAPE):
            
