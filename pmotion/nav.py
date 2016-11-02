import collections
import math

import motor_params

State = collections.namedtuple("State", ["x", "y", "theta"])
Dest = collections.namedtuple("Dest", ["x", "y"])


def navigateToWaypoint(state, dest):
    goal_theta = math.atan2(dest.y - state.y, dest.x - state.x)
    delta_theta_rad = state.theta - goal_theta
    if delta_theta_rad > math.pi:
        delta_theta_rad = 2*math.pi - delta_theta_rad
    motor_params.rotate(delta_theta_rad / math.pi * 180.0)
    new_theta = goal_theta
    dist = math.sqrt((state.y - dest.y)**2 + (state.x - dest.x)**2)
    motor_params.forward(dist)

    return State(x=dest.x, y=dest.y, theta=new_theta)


def main():
    state = State(x=0, y=0, theta=0)
    
    while True:
        args = raw_input("Enter a destination waypoint")
        x, y = args.strip().split()
        dest = Dest(x=float(x), y=float(y))
        state = navigateToWaypoint(state, dest)


if __name__ == "__main__":
    main()
