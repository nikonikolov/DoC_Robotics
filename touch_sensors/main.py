"""Module for Practical 3: Investigating sensors."""

import time

import brickpi

import motor_params


TOUCH_PORT_LEFT = 1
TOUCH_PORT_RIGHT = 0
FORWARD_SPEED = 5.0
STATE_DRIVE = 0
STATE_LEFT_BUMP = 1
STATE_RIGHT_BUMP = 2
STATE_BOTH_BUMP = 3
STATE_LEFT_BACKTRACK = 4
STATE_RIGHT_BACKTRACK = 5


interface = motor_params.interface


def execute_state_transition(unused_old_state, new_state):
    # Clean up things from the old state
    interface.setMotorPwm(0, 0)
    interface.setMotorPwm(1, 0)
    time.sleep(0.4)

    # Start entering the new state
    if new_state == STATE_DRIVE:
        interface.setMotorRotationSpeedReferences(
                motor_params.motors, [FORWARD_SPEED, FORWARD_SPEED])
    elif new_state in [STATE_BOTH_BUMP, STATE_LEFT_BUMP, STATE_RIGHT_BUMP]:
        angle = motor_params.dist_to_motor_angle(-5)
        interface.increaseMotorAngleReferences(motor_params.motors, [angle, angle])
    elif new_state == STATE_LEFT_BACKTRACK:
        angle = motor_params.rotate_left_to_motor_angle(45)
        interface.increaseMotorAngleReferences(motor_params.motors, [angle, -angle])
    elif new_state == STATE_RIGHT_BACKTRACK:
        angle = motor_params.rotate_right_to_motor_angle(45)
        interface.increaseMotorAngleReferences(motor_params.motors, [-angle, angle])
    else:
        raise RuntimeError("Unknown state")


def navigate(state):
    if state == STATE_DRIVE:
        left = interface.getSensorValue(TOUCH_PORT_LEFT)
        right = interface.getSensorValue(TOUCH_PORT_RIGHT)
        next_state = left[0] + (right[0] << 1)

    elif state == STATE_LEFT_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.motors)
        next_state = STATE_LEFT_BACKTRACK if done else state

    elif state == STATE_RIGHT_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.motors)
        next_state = STATE_RIGHT_BACKTRACK if done else state

    elif state == STATE_BOTH_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.motors)
        next_state = STATE_LEFT_BACKTRACK if done else state

    elif state == STATE_LEFT_BACKTRACK:
        done = interface.motorAngleReferencesReached(
                motor_params.motors)
        next_state = STATE_DRIVE if done else state

    elif state == STATE_RIGHT_BACKTRACK:
        done = interface.motorAngleReferencesReached(motor_params.motors)
        next_state = STATE_DRIVE if done else state

    else:
        raise RuntimeError("Unknown state")

    if state != next_state:
        execute_state_transition(state, next_state)

    return next_state


def main():
    interface.sensorEnable(TOUCH_PORT_LEFT, brickpi.SensorType.SENSOR_TOUCH)
    interface.sensorEnable(TOUCH_PORT_RIGHT, brickpi.SensorType.SENSOR_TOUCH)
    interface.setMotorRotationSpeedReferences(
            motor_params.motors, [FORWARD_SPEED, FORWARD_SPEED])
    current_state = STATE_DRIVE
    while True:
        current_state = navigate(current_state)


main()
