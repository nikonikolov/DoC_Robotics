"""Module for Practical 3: Investigating sensors."""

import time

import brickpi

import motor_params


TOUCH_PORT_LEFT = 1
TOUCH_PORT_LEFT = 2
FORWARD_SPEED = 12.0
STATE_DRIVE = 0
STATE_LEFT_BUMP = 1
STATE_RIGHT_BUMP = 2
STATE_BOTH_BUMP = 3

interface = motor_params.interface


def execute_state_transition(unused_old_state, new_state):
    # Clean up things from the old state
    interface.setMotorPwm(0, 0)
    interface.setMotorPwm(1, 0)
    time.sleep(0.4)

    # Start entering the new state
    if old_state == STATE_DRIVE:
        interface.setRotationSpeedReference(motor_params.motors,
                                            [FORWARD_SPEED, FORWARD_SPEED])
    elif old_state == STATE_LEFT_BUMP:
        angle = motor_params.rotate_right_to_motor_angle(-45.0)
        interface.increaseMotorAngleReferences(1, angle)
    elif old_state == STATE_RIGHT_BUMP:
        angle = motor_params.rotate_right_to_motor_angle(-45.0)
        interface.increaseMotorAngleReferences(0, angle)
    elif old_state == STATE_BOTH_BUMP:
        angle = motor_params.rotate_right_to_motor_angle(-45.0)
        interface.increaseMotorAngleReferences(1, angle)
    else:
        raise RuntimeError("Unknown state")


def navigate(state):
    if state == STATE_DRIVE:
        left = interface.getSensorValue(TOUCH_PORT_LEFT)
        right = interface.getSensorValue(TOUCH_PORT_RIGHT)
        next_state = left + (right >> 1)

    elif state == STATE_LEFT_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.MOTOR_RIGHT)
        next_state = STATE_DIRVE if done else state

    elif state == STATE_RIGHT_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.MOTOR_LEFT)
        next_state = STATE_DIRVE if done else state

    elif state == STATE_BOTH_BUMP:
        done = interface.motorAngleReferencesReached(
                motor_params.LEFT)
        next_state = STATE_DIRVE if done else state

    else:
        raise RuntimeError("Unknown state")

    if state != next_state:
        execute_state_transition(state, next_state)

    return navigate(next_state)


def main():
    interface.sensorEnable(TOUCH_PORT, brickpi.SensorType.SENSOR_TOUCH)

    interface.setRotationSpeedReference(motor_params.motors,
                                        [FORWARD_SPEED, FORWARD_SPEED])
    navigate(FORWARD_SPEED)


main()
