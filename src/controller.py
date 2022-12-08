import pygame
import settings as s
import scene
from sound import SoundManager
import sys

class GameController:
    """The Controller object is the heart of this program. It contains our main game loop.
    Tick Clock, Handle Events, Update Game State, Render Graphics, Check for any environment changes.
    The main game loop is the Controller's run method."""
    def __init__(self):
        
        pygame.init()
        self.display = self._get_display()
        self.clock = self._get_clock()
        self.sceneManager = self._get_SceneManager()
        self.soundManager = SoundManager()
        
        # self.event_handler = EventHandler()
        self.running = True

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
        mainMenu = scene.MainMenuScene()
        sceneManager.push(mainMenu)
        
        return sceneManager

    def run(self):
        """The main game loop that continuously runs after the game has been initialized."""
        while self.running:
            
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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.KEYDOWN and\
                event.key == pygame.K_ESCAPE):
                self.running = False
                
                pygame.quit()
                sys.exit()    
                
    # def try_quit(e):
    #     if e.type == QUIT or\
    #     (e.type == KEYDOWN and\
    #     e.key == K_ESCAPE):
            

    # def update_state(self):
    #     self.state.update()
    #     if self.state.is_done:
    #         self.previous_state = self.state
    #         self.state = self.game_states[self.previous_state.next_state](persist=self.previous_state.persist)
    #         self.previous_state.cleanup()

    # def render_state(self):
    #     self.state.render(self.display)

    # def check_env_changes(self):
    #     """Checks to see if any environment changes occur during a single loop of the game. Examples below:
    #     Connecting/Disconnecting input devices
    #     Changing audio device
    #     Resolution / Window resize"""
    #     self.check_input_device_change()
    #     self.check_audio_device_change()
    #     self.check_resolution_change()

    # def check_input_device_change(self):
    #     pass

    # def check_audio_device_change(self):
    #     pass

    # def check_resolution_change(self):
    #     pass