#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Direction, Stop

import socket
import time
import json

import moves

PASSWORD = "ev3pass"
HOST = "24.199.72.202"
PORT = 5555

FORWARD_SPEED = 800
BACK_SPEED = FORWARD_SPEED
TURN_SPEED = 800
CAMERA_SPEED = 50

CAMERA_LIMIT_DEG = 60

right_motor = Motor(Port.A, Direction.CLOCKWISE)
left_motor = Motor(Port.D, Direction.CLOCKWISE)

camera_motor = Motor(Port.B, Direction.CLOCKWISE)
camera_sensor =  TouchSensor(Port.S2)

def drive(state):
    left = 0
    right = 0

    if state[moves.MOVE_FORWARD]:
        left = FORWARD_SPEED
        right = FORWARD_SPEED

    elif state[moves.MOVE_BACK]:
        left = BACK_SPEED * -1
        right = BACK_SPEED * -1

    if state[moves.MOVE_LEFT] and state[moves.MOVE_RIGHT]:
        pass

    elif state[moves.MOVE_RIGHT] and not (state[moves.MOVE_FORWARD] or state[moves.MOVE_FORWARD]):
        left = TURN_SPEED
        right = TURN_SPEED // -1.1

    elif state[moves.MOVE_LEFT] and not (state[moves.MOVE_FORWARD] or state[moves.MOVE_FORWARD]):
        right = TURN_SPEED
        left = TURN_SPEED // -1.1

    elif state[moves.MOVE_LEFT]:
        right += TURN_SPEED
        left -= TURN_SPEED // 1.3

    elif state[moves.MOVE_RIGHT]:
        left += TURN_SPEED
        right -= TURN_SPEED // 1.3

    print(left)
    print(right)
    print()

    left_motor.run(left)
    right_motor.run(right)

def move_camera(state):
    camera = 0

    if state[moves.CAMERA_UP] and state[moves.CAMERA_DOWN]:
        pass

    elif state[moves.CAMERA_UP] and not camera_sensor.pressed():
        camera -= CAMERA_SPEED

    elif state[moves.CAMERA_DOWN] and camera_motor.angle() <= CAMERA_LIMIT_DEG:
        camera += CAMERA_SPEED

    camera_motor.run(camera)

def start_vehicle(s):
    while True:
        s.sendall("get".encode())
        data = s.recv(512)
        moves_json = data.decode("utf-8")

        move_state = json.loads(moves_json)

        print("State: " + str(move_state))

        drive(move_state)
        move_camera(move_state)

        msleep(20)

def init():
    print("Intitilizing camera motor...")

    camera_motor.run(-50)

    pressed = False
    while not pressed:
        pressed = camera_sensor.pressed()

    camera_motor.run(0)
    camera_motor.reset_angle(0)
    camera_motor.run_angle(50, 0, then=Stop.COAST)

    print("Done.")

def msleep(t):
    time.sleep(t / 1000)

def main():
    # Initialize the EV3 Brick.
    ev3 = EV3Brick()

    init()

    print("Connecting to " + HOST + ":" + str(PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall(PASSWORD.encode())
    auth_status = s.recv(1024).decode("utf-8")
    if auth_status == "connected":
        print("Authenticated succesfully!")
        start_vehicle(s)

    else:
        print("Authentication failed!")

if __name__ == "__main__":
    main()
