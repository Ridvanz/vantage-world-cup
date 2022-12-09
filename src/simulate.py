import numpy as np
from utils import clip

class Player():
    def __init__(self):
    
        pass


def simulate_shot(shooter, keeper, u_x, u_c):

    u_x = clip(u_x, -1, 1)
    u_c = clip(u_c, -1, 1)

    goal_x = 400
    dist_x = goal_x * u_x
    dist_c = goal_x * u_c
    dist_y = -700
    ball_radius = 30

    straight_sigma = 4000 / (5 + shooter.accuracy)
    curve_sigma = abs(
        dist_c / 20 + straight_sigma * dist_c / 400 * (1 - shooter.curve / 100)
    )
    duration = 70 - int(shooter.power**0.5) * 5

    frames = np.linspace(0, 1, duration)

    deviation = np.random.normal(scale=straight_sigma + curve_sigma)
    destination = dist_x + deviation
    ball_x = frames * (destination + dist_c) - frames**2 * dist_c
    ball_y = frames * dist_y

    keeper_speed = 5 + keeper.speed / 10
    keeper_acceleration = keeper_speed / 10

    p_gain = 0.5
    d_gain = 1

    initial_guess = np.random.normal(scale=200)

    keeper_x = [0]
    keeper_vx = 0

    target = (
        frames * destination
        + (1 - frames) * ball_x
        + (1 - frames) * (2 - keeper.predict / 100) * initial_guess
    )

    error = 0

    for x in target:

        previous_error = error
        error = x - keeper_x[-1]

        delta_error = error - previous_error

        keeper_ax = error * p_gain + delta_error * d_gain

        keeper_vx += clip(keeper_ax, -keeper_acceleration, keeper_acceleration)
        keeper_vx = clip(keeper_vx, -keeper_speed, keeper_speed)
        keeper_x_clipped = clip(keeper_x[-1] + keeper_vx, -goal_x - 100, goal_x + 100)

        keeper_x.append(keeper_x_clipped)

    goal = (
        abs(ball_x[-1] - keeper_x[-1]) > (ball_radius + keeper.keeper_radius)
        and ball_x[-1] > -goal_x
        and ball_x[-1] < goal_x
    )

    return goal, ball_x, ball_y, keeper_x, target



def simulation(shooter_stats = (50,50,50), keeper_stats = (50,50,50),  u_x = 0, u_c = 0):
    
    #simulate a single shot with stats and shot parameters
    
    shooter = Player()
    shooter.power = shooter_stats[0]
    shooter.accuracy = shooter_stats[1]
    shooter.curve = shooter_stats[2]
    
    keeper = Player()
    keeper.reach = shooter_stats[0]
    keeper.speed = shooter_stats[1]
    keeper.predict = shooter_stats[2]
    
    
    shooter.shooter_radius = 40 + shooter.power/4
    keeper.keeper_radius = 40 + keeper.reach/4
    
    goal, ball_x, ball_y, keeper_x, _ = simulate_shot(shooter, keeper, u_x, u_c)
        
    return goal, ball_x, ball_y, keeper_x


