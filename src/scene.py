import pygame
import utils
import settings as s
from pygame import Color
from utils import HSV, clip
import numpy as np
from enum import Enum
from entities import Player
import sys
from simulate import simulate_shot
import pygame.gfxdraw

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


class State(Enum):
    TARGET = 1
    CURVE = 2
    CONFIRM = 3
    RUN = 4
    SHOOT = 5
    WIN = 6


class PenaltyScene(Scene):
    def __init__(self, P1, P2, round):
        # self.window = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
        self.round = round
        self.P1 = P1
        self.P2 = P2
        self.window = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
        self.field_color = HSV(h=0)
        self.goal_x = 400
        self.goal_size = 800
        self.penalty_area_width = 800
        self.penalty_area_width = 400
        self.mousepos = None
        self.ticks = 0
        self.ball_start = (s.WINDOW_WIDTH / 2, 800)
        self.top_space = 100
        self.bottom_space = 55
        self.side_space = 100
        self.state = State.TARGET
        self.max_curve = 800
        self.enter = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.next = True
        self.previous = True
        self.ball_radius = 30
        self.shooter_speed = 10
        self.max_goals = 4

    def onEnter(self):
        # globals.soundManager.playMusicFade('solace')

        self.even_round = self.round % 2

        if self.even_round:
            self.shooter = self.P1
            self.keeper = self.P2
        else:
            self.shooter = self.P2
            self.keeper = self.P1

        self.dist_x = 0
        self.curve_x = 0
        self.keeper_target = 0
        self.dist_y = self.top_space - self.ball_start[1]

        self.ball_x, self.ball_y = self.ball_start

        self.keeper_x = s.WINDOW_WIDTH / 2
        self.shooter_x = s.WINDOW_WIDTH / 2

        self.keeper_y = self.top_space
        self.shooter_y = s.WINDOW_HEIGHT - self.bottom_space

    def input(self, sm):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.next = True
                elif event.button == 3:
                    self.previous = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.enter = True

                else:
                    self.enter = False

            if event.type == pygame.QUIT:
                self.running = False

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sm.scenes.append(PauseScene())

    def update(self, sm):

        if self.state == State.TARGET:

            self.dist_x = self.mouse_x - s.SCREEN_WIDTH / 2
            self.dist_x = clip(self.dist_x, -400, 400)

            if self.next:
                self.state = State.CURVE
                self.next = False

        elif self.state == State.CURVE:

            self.curve_x = self.mouse_x - s.SCREEN_WIDTH / 2 - self.dist_x
            self.curve_x = clip(self.curve_x, -self.max_curve, self.max_curve)

            if self.next:
                self.state = State.CONFIRM
                self.next = False
            elif self.previous:
                self.state = State.TARGET
                self.previous = False
                self.curve_x = 0

        elif self.state == State.CONFIRM:

            (
                self.goal,
                self.ball_trajectory_x,
                self.ball_trajectory_y,
                self.keeper_trajectory_x,
                self.keeper_target_x,
            ) = simulate_shot(
                self.shooter, self.keeper, self.dist_x / 400, self.curve_x / 400
            )

            if self.next:
                self.state = State.RUN
                self.next = False
            elif self.previous:
                self.state = State.CURVE
                self.previous = False

        elif self.state == State.RUN:

            self.shooter_y -= self.shooter_speed
            if self.shooter_y < (self.ball_start[1] + 2 * self.ball_radius):
                self.state = State.SHOOT
                self.ticks = 0

        elif self.state == State.SHOOT:

            i = self.ticks
            self.ball_x = self.ball_start[0] + self.ball_trajectory_x[i]
            self.ball_y = self.ball_start[1] + self.ball_trajectory_y[i]

            self.keeper_x = self.ball_start[0] + self.keeper_trajectory_x[i]
            self.keeper_target = self.ball_start[0] + self.keeper_target_x[i]

            self.ticks += 1

            if self.ticks > len(self.ball_trajectory_y) - 1:
                self.state = State.WIN

                if self.goal:
                    self.shooter.scored()

                else:
                    self.keeper.scored()

        elif self.state == State.WIN:

            if self.enter:

                if self.P1.score < self.max_goals and self.P2.score < self.max_goals:

                    self.round += 1
                    scene = PenaltyScene(self.P1, self.P2, self.round)
                    sm.pop()

                else:

                    winner = self.P1 if self.P1.score > self.P2.score else self.P2
                    scene = WinnerScene(winner)

                sm.push(scene)

    def render(self, sm):
        sm.display.fill(s.BLACK)
        #
        self.draw_field()

        if self.state == State.TARGET or self.state == State.CURVE:
            self.draw_name()
            self._draw_trajectories(HSV(0, 80, 90), 5)

        if self.state == State.CONFIRM:
            self._draw_trajectories(HSV(240, 80, 90))

        elif self.state == State.SHOOT:

            pygame.draw.circle(
                self.window, s.ORANGE, (self.keeper_target, self.top_space), 30, 3
            )

        self.draw_ball()

        if self.state == State.WIN:
            if self.goal:
                self.draw_ball(s.GREEN)
            else:
                self.draw_ball(s.RED)

        self.draw_shooter()
        self.draw_keeper()

        self.draw_scoreboard(sm)

        sm.display.blit(
            self.window,
            (
                (s.SCREEN_WIDTH - s.WINDOW_WIDTH) / 2,
                (s.SCREEN_HEIGHT - s.WINDOW_HEIGHT) / 2,
            ),
        )

    def draw_name(self):

        font = pygame.font.SysFont("Arial", 50)
        text = font.render(f"{self.shooter.name}", True, (120, 120, 255))
        self.window.blit(
        text, (s.WINDOW_WIDTH / 2 + 100,  s.WINDOW_HEIGHT / 2 + 100)
        )

    def draw_scoreboard(self, sm):

        scores_x = 75
        scores_radius = 50

        for i in range(self.max_goals):

            if i < self.P1.score:
                pygame.draw.circle(
                    sm.display,
                    self.P1.colors[0],
                    (scores_x, 100 + i * 150),
                    scores_radius,
                )

            if i < self.P2.score:
                pygame.draw.circle(
                    sm.display,
                    self.P2.colors[0],
                    (s.SCREEN_WIDTH - scores_x, 100 + i * 150),
                    scores_radius,
                )
            pygame.draw.circle(
                sm.display,
                self.P1.colors[1],
                (scores_x, 100 + i * 150),
                scores_radius,
                10,
            )

            pygame.draw.circle(
                sm.display,
                self.P2.colors[1],
                (s.SCREEN_WIDTH - scores_x, 100 + i * 150),
                scores_radius,
                10,
            )

    def draw_ball(self, color=s.ORANGE):
        pygame.draw.circle(
            self.window, color, (self.ball_x, self.ball_y), self.ball_radius
        )

        pygame.draw.circle(
            self.window, s.BLACK, (self.ball_x, self.ball_y), self.ball_radius, 5
        )

    def draw_shooter(self):
        pygame.draw.circle(
            self.window,
            self.shooter.colors[0],
            (self.shooter_x, self.shooter_y),
            self.shooter.shooter_radius,
        )

        pygame.draw.circle(
            self.window,
            self.shooter.colors[1],
            (self.shooter_x, self.shooter_y),
            self.shooter.shooter_radius,
            15,
        )

    def draw_keeper(self):

        pygame.draw.circle(
            self.window,
            self.keeper.colors[0],
            (self.keeper_x, self.keeper_y),
            self.keeper.keeper_radius,
        )

        pygame.draw.circle(
            self.window,
            self.keeper.colors[1],
            (self.keeper_x, self.keeper_y),
            self.keeper.keeper_radius,
            15,
        )

    def draw_field(self):

        self.window.fill(HSV(120, 80, 100))

        pygame.draw.rect(
            self.window,
            s.WHITE,
            (-50, 100, (s.WINDOW_WIDTH + 100), (s.WINDOW_HEIGHT)),
            10,
        )
        pygame.draw.rect(
            self.window,
            s.WHITE,
            (50, 100, (s.WINDOW_WIDTH - 2 * 50), (s.WINDOW_HEIGHT - 2 * 50 - 50)),
            10,
        )
        pygame.draw.rect(
            self.window, s.WHITE, (self.goal_x, -50, self.goal_size, 160), 10
        )

        pygame.draw.circle(self.window, s.WHITE, (s.WINDOW_WIDTH / 2, 800), 10)

    def _get_trajectory(self, dist_x, dist_y, curve_x, power, accuracy, curve):

        straight_sigma = 4000 / (5 + accuracy)

        curve_sigma = abs(
            curve_x / 20 + straight_sigma * curve_x / 400 * (1 - curve / 100)
        )

        duration = 70 - int(power**0.5) * 4

        frames = np.linspace(0, 1, duration)

        ball_y = frames * dist_y

        ball_x_mean = frames * (dist_x + curve_x) - frames**2 * curve_x
        ball_x_left = (
            frames * (dist_x + curve_x - 3 * (straight_sigma + curve_sigma))
            - frames**2 * curve_x
        )
        ball_x_right = (
            frames * (dist_x + curve_x + 3 * (straight_sigma + curve_sigma))
            - frames**2 * curve_x
        )

        return ball_y, ball_x_mean, ball_x_left, ball_x_right

    def _draw_trajectories(self, color, width=10):

        (
            trajectory_y,
            trajectory_x_mean,
            trajectory_x_left,
            trajectory_x_right,
        ) = self._get_trajectory(
            self.dist_x,
            self.dist_y,
            self.curve_x,
            self.shooter.power,
            self.shooter.accuracy,
            self.shooter.curve,
        )

        for traj in [trajectory_x_mean, trajectory_x_left, trajectory_x_right]:

            coords = [
                (self.ball_start[0] + traj[i], self.ball_start[1] + trajectory_y[i])
                for i in range(len(trajectory_y))
            ]
            pygame.draw.lines(self.window, color, False, coords, width=width)

        # for entity in self.all_sprites:
        #     self.window.blit(entity.surf, entity.rect)


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
        sm.display.fill(s.BLACK)

        font = pygame.font.SysFont("Arial", 16)
        fps = font.render(f"Welcome", True, (255, 255, 255))
        sm.display.blit(fps, (820, 800))


class IntroScene(Scene):
    def __init__(self):
        self.window_height = 1920
        self.window_width = 1080

        self.window = pygame.Surface((self.window_width, self.window_height))

        self.window.fill(HSV(120, 80, 20))

        # pygame.draw.rect(self.window, color, pygame.Rect(30, 30, 60, 60))

    def update(self, sm):
        pass

    def input(self, sm):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    sm.push(PenaltyScene(sm.P1, sm.P2, 0))

    def render(self, sm):

        sm.display.fill(s.BLACK)

        font = pygame.font.SysFont("Arial", 100)
        text = font.render(f"Vantage World Cup", True, s.ORANGE)
        self.window.blit(
            text, (self.window_width / 2 - 350, self.window_height / 2 - 200)
        )

        sm.display.blit(
            self.window,
            (
                (s.SCREEN_WIDTH - self.window_width) / 2,
                (s.SCREEN_HEIGHT - self.window_height) / 2,
            ),
        )


class PauseScene(Scene):
    def __init__(self):
        self.window_height = 700
        self.window_width = 1000

        self.window = pygame.Surface((self.window_width, self.window_height))

    def update(self, sm):
        pass

    def input(self, sm):

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sm.scenes.pop()

                elif event.key == pygame.K_q:

                    pygame.quit()
                    sys.exit()

    def render(self, sm):

        # sm.display.fill(s.BLACK)

        font = pygame.font.SysFont("Arial", 100)
        text = font.render(f"Game Paused", True, (255, 255, 255))
        self.window.blit(
            text, (self.window_width / 2 - 250, self.window_height / 2 - 200)
        )

        font = pygame.font.SysFont("Arial", 80)
        text = font.render(f"Press Q to quit", True, (255, 255, 255))
        self.window.blit(text, (self.window_width / 2 - 200, self.window_height / 2))

        sm.display.blit(
            self.window,
            (
                (s.SCREEN_WIDTH - self.window_width) / 2,
                (s.SCREEN_HEIGHT - self.window_height) / 2,
            ),
        )


class WinnerScene(Scene):
    def __init__(self, winner):
        self.winner = winner
        self.window_height = 800
        self.window_width = 1600

        self.window = pygame.Surface((self.window_width, self.window_height))

        self.window.fill(HSV(180, 50, 50))

    def update(self, sm):
        pass

    def input(self, sm):

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

    def render(self, sm):
        font = pygame.font.SysFont("Arial", 100)
        text = font.render(f"{self.winner.name} wins!", True, (255, 255, 255))
        self.window.blit(
            text, (self.window_width / 2 - 300, self.window_height / 2 - 200)
        )

        sm.display.blit(
            self.window,
            (
                (s.SCREEN_WIDTH - self.window_width) / 2,
                (s.SCREEN_HEIGHT - self.window_height) / 2,
            ),
        )
