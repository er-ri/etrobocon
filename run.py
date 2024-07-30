#!/usr/bin/env python3

import cv2
import time
import socket
import pickle
import struct
from etrobocon.unit import ETRobot
from etrobocon.utils import steer_by_camera, PIDController

# User defined constants
FILE_LABEL = int(time.time())  # Label for saved camera capture and steering data
SPECIFIED_FPS = 20  # Camera capturing fps
DELTA_TIME = 1 / SPECIFIED_FPS  # Interval between two frames (used by PID controller)
POWER = 35  # Motor power
SEND_CAPTURE = True  # Whether to send the camera capture
HOST_IP_ADDRESS = (
    "192.168.0.45"  # The destination IP that the Raspberry Pi will send to
)

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, SPECIFIED_FPS)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(
    filename=f"storage/{FILE_LABEL}_picamera.avi",
    fourcc=fourcc,
    fps=20.0,
    frameSize=(640, 480),
)


# Driving data recorder
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video

# Socket connection for sending camera capture
if SEND_CAPTURE:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST_IP_ADDRESS, 8485))


def run_one_frame(delta_time: float) -> None:
    ret, frame = cap.read()
    out.write(frame)

    roi = frame[300:, :]

    steer, info = steer_by_camera(roi=roi)

    steer = pid.update(steer, delta_time=delta_time)

    left_power = POWER + steer
    right_power = POWER - steer

    et.set_motor_power(left_power=left_power, right_power=right_power)

    if SEND_CAPTURE:
        ret, buffer = cv2.imencode(".png", frame)
        img_encoded = buffer.tobytes()
        data = pickle.dumps(img_encoded)
        client_socket.sendall(struct.pack("L", len(data)) + data)


pid = PIDController(Kp=0.7, Ki=0.1, kd=0, setpoint=0)
et = ETRobot()

# Start
run_one_frame(delta_time=0)


while et.is_running == True:
    run_one_frame(delta_time=DELTA_TIME)

    if cv2.waitKey(0) & 0xFF == ord("q"):
        break

et.stop()

cap.release()
out.release()
