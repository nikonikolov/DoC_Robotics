import motor_params
import math

def navigateToWaypoint(state, dest):
	ugoal_theta = atan2((state.y-dest.y)/(state.x-dest.x))
	delta_theta_rad = state.theta - goal_theta
	if delta_theta_rad > math.pi:
		delta_theta_rad = 2*math.pi - delta_theta_rad
	motor_params.rotate(delta_theta_rad/math.pi*180)
	state.theta = goal.theta
	dist = sqrt((state.y - dest.y)**2 + (state.x - dest.x)**2)
	motor_params.forward(dist)

	return state


def main():
	state.x = 0
	state.y = 0
	state.theta = 0
	
	while true:
		args = input("Enter a destination waypoint")	
		dest_list = args.split()
		dest.x = float(dest_list[0])
		dest.y = float( dest_list[1])
		state = navigateToWaypint(state, dest)

	
	
