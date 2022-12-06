import pygame
import utils
import settings as s

class SceneManager:
    def __init__(self, display):
        self.display = display
        self.scenes = []
    def isEmpty(self):
        return len(self.scenes) == 0
    
    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()
    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()
            
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self)
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)
    def render(self):
        if len(self.scenes) > 0:
            self.scenes[-1].render(self)
        # present screen
        pygame.display.flip()
        
    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()
         
    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()
        
    def set(self, scenes):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scenes
        for s in scenes:
            self.push(s)


class Scene:
    def __init__(self):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass
    def input(self, sm):
        pass
    def update(self, sm):
        pass
    def render(self, sm):
        pass

class MainMenuScene(Scene):
    def __init__(self):
        # self.enter = ui.ButtonUI(pygame.K_RETURN, '[Enter=next]', 50, 200)
        # self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 250)
        pass
    
    def onEnter(self):
        # globals.soundManager.playMusicFade('solace')
        pass
    
    def input(self, sm):
        # if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
        #     sm.push(FadeTransitionScene([self], [PlayerSelectScene()]))
        # if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
        #     sm.pop()
        
        
        for event in pygame.event.get():
                
                # Condition becomes true when keyboard is pressed   
                if event.type == pygame.KEYDOWN:
        
                    if event.key == pygame.K_RETURN:
                        sm.push(PenaltyScene())
        
        
    def update(self, sm):
        # self.enter.update(inputStream)
        # self.esc.update(inputStream)
        pass
    
    def render(self, sm):
        # background
        sm.display.fill(s.WHITE)
        # utils.drawText(screen, 'Main Menu', 50, 50, globals.WHITE, 255)
        # self.enter.draw(screen)
        # self.esc.draw(screen)




        red = max(0,min(255, self.player.v_y*5))
        self.window.fill((red, 255, 255-red))
    
        for entity in self.all_sprites:
            self.window.blit(entity.surf, entity.rect)
            
        self.window.blit(self.player.surf, self.player.rect)
        
        self.screen.fill(s.BLACK)
        self.screen.blit(self.window, ((s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2, (s.SCREEN_HEIGHT-s.WINDOW_HEIGHT)/2))
        
        font = pygame.font.SysFont('Arial', 16)
        fps = font.render(f"FPS: {round(self.clock.get_fps(),2)}", True, (255,255,255))
        speed = font.render(f"Speed: {round(self.player.v_y,1)}",True,(255,255,255))
        ticks = font.render(f"Ticks: {self.ticks}",True,(255,255,255))
        distance_left = font.render(f"Distance left: {int(s.TRACK_LENGTH-self.player.s_y)}",True,(255,255,255))
        
        self.screen.blit(fps,(820,20))
        self.screen.blit(speed, (820, 60))
        self.screen.blit(ticks, (820, 100))
        self.screen.blit(distance_left,(820,140))
        
        pygame.display.update()
        
        self.clock.tick(s.FPS)




# class PenaltyScene(Scene):
#     def __init__(self):
#         self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 300)
#     def onEnter(self):
#         globals.soundManager.playMusicFade('solace')
#     def update(self, sm, inputStream):
#         self.esc.update(inputStream)
#     def input(self, sm, inputStream):
#         if inputStream.keyboard.isKeyPressed(pygame.K_a):
#             globals.curentLevel = max(globals.curentLevel-1, 1)
#         if inputStream.keyboard.isKeyPressed(pygame.K_d):
#             globals.curentLevel = min(globals.curentLevel+1, globals.lastCompletedLevel)
#         if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
#             level.loadLevel(globals.curentLevel)
#             sm.push(FadeTransitionScene([self], [GameScene()]))

#         if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
#             sm.pop()
#             sm.push(FadeTransitionScene([self], []))
#     def draw(self, sm, screen):
#         # background
#         screen.fill(globals.DARK_GREY)
#         utils.drawText(screen, 'Level Select', 50, 50, globals.WHITE, 255)
#         self.esc.draw(screen)

#         # draw level select menu
#         for levelNumber in range(1, globals.maxLevel+1):
#             c = globals.WHITE
#             if levelNumber == globals.curentLevel:
#                 c = globals.GREEN
#             a = 255
#             if levelNumber > globals.lastCompletedLevel:
#                 a = 100
#             utils.drawText(screen, str(levelNumber), levelNumber*100, 100, c, a)

class PlayerSelectScene(Scene):
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, '[Enter=next]', 50, 200)
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 250)
    def onEnter(self):
        globals.soundManager.playMusicFade('solace')
    def update(self, sm, inputStream):
        self.esc.update(inputStream)
        self.enter.update(inputStream)
    def input(self, sm, inputStream):

        # handle each player
        for player in [globals.player1, globals.player2, globals.player3, globals.player4]:

            # add to the game
            if inputStream.keyboard.isKeyPressed(player.input.b1):
                if player not in globals.players:
                    globals.players.append(player)
            
            # remove from the game
            if inputStream.keyboard.isKeyPressed(player.input.b2):
                if player in globals.players:
                    globals.players.remove(player)

        #print(len(globals.players))

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            if len(globals.players) > 0:
                utils.setPlayerCameras()
                sm.push(FadeTransitionScene([self], [LevelSelectScene()]))

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
            
    def draw(self, sm, screen):
        # background
        screen.fill(globals.DARK_GREY)
        utils.drawText(screen, 'Player Select', 50, 50, globals.WHITE, 255)

        self.esc.draw(screen)
        self.enter.draw(screen)

        # draw active players

        if globals.player1 in globals.players:
            screen.blit(utils.playing, (100,100))
        else:
            screen.blit(utils.not_playing, (100,100))
        
        if globals.player2 in globals.players:
            screen.blit(utils.playing, (150,100))
        else:
            screen.blit(utils.not_playing, (150,100))

        if globals.player3 in globals.players:
            screen.blit(utils.playing, (200,100))
        else:
            screen.blit(utils.not_playing, (200,100))

        if globals.player4 in globals.players:
            screen.blit(utils.playing, (250,100))
        else:
            screen.blit(utils.not_playing, (250,100))
        
class GameScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = engine.CollectionSystem()
        self.battleSystem = engine.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()
        self.powerupSystem = engine.PowerupSystem()
    def onEnter(self):
        globals.soundManager.playMusicFade('dawn')
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            # update the level select map accessible levels
            nextLevel = min(globals.curentLevel+1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())
    def update(self, sm, inputStream):
        self.inputSystem.update(inputStream=inputStream)
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()
        self.powerupSystem.update()
    def draw(self, sm, screen):
        # background
        screen.fill(globals.DARK_GREY)
        self.cameraSystem.update(screen)

class WinScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface((830,830))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        utils.drawText(screen, 'You win!', 50, 50, globals.WHITE, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

class LoseScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Esc=quit]', 50, 200)
    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])
    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface((830,830))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0,0), self.alpha * 0.7)

        utils.drawText(screen, 'You lose!', 150, 150, globals.WHITE, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)

class TransitionScene(Scene):
    def __init__(self, fromScenes, toScenes):
        self.currentPercentage = 0
        self.fromScenes = fromScenes
        self.toScenes = toScenes
    def update(self, sm, inputStream):
        self.currentPercentage += 2
        if self.currentPercentage >= 100:
            sm.pop()
            for s in self.toScenes:
                sm.push(s)
        for scene in self.fromScenes:
            scene.update(sm, inputStream)
        if len(self.toScenes) > 0:
            for scene in self.toScenes:
                scene.update(sm, inputStream)
        else:
            if len(sm.scenes) > 1:
                sm.scenes[-2].update(sm, inputStream)

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm, screen)
            else:
                for s in self.toScenes:
                    s.draw(sm, screen)

        # fade overlay
        overlay = pygame.Surface((830,830))
        alpha = int(abs((255 - ((255/50)*self.currentPercentage))))
        overlay.set_alpha(255 - alpha)
        overlay.fill(globals.BLACK)
        screen.blit(overlay, (0,0))
        
class PenaltyScene(Scene):
    def __init__(self):
        pass
    def update(self, sm):
        pass
    def input(self, sm):
        pass
    
    def draw(self, sm):
        
        red = max(0,min(255, self.player.v_y*5))
        self.window.fill((red, 255, 255-red))
    
        for entity in self.all_sprites:
            self.window.blit(entity.surf, entity.rect)
            
        self.window.blit(self.player.surf, self.player.rect)
        
        self.screen.fill(s.BLACK)
        self.screen.blit(self.window, ((s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2, (s.SCREEN_HEIGHT-s.WINDOW_HEIGHT)/2))
        
        font = pygame.font.SysFont('Arial', 16)
        fps = font.render(f"FPS: {round(self.clock.get_fps(),2)}", True, (255,255,255))
        speed = font.render(f"Speed: {round(self.player.v_y,1)}",True,(255,255,255))
        ticks = font.render(f"Ticks: {self.ticks}",True,(255,255,255))
        distance_left = font.render(f"Distance left: {int(s.TRACK_LENGTH-self.player.s_y)}",True,(255,255,255))
        
        self.screen.blit(fps,(820,20))
        self.screen.blit(speed, (820, 60))
        self.screen.blit(ticks, (820, 100))
        self.screen.blit(distance_left,(820,140))
    
    
class WinnerScene(Scene):
    def __init__(self):
        pass
    def update(self, sm):
        pass
    def input(self, sm):
        pass
    
    def draw(self, sm):
        pass
    
    
    
class IntroScene(Scene):
    def __init__(self):
        pass
    def update(self, sm):
        pass
    def input(self, sm):
        pass
    
    def draw(self, sm):
        pass
    
    
class PenaltyScene(Scene):
    def __init__(self):
        pass
    def update(self, sm):
        pass
    def input(self, sm):
        pass
    
    def draw(self, sm):
        pass