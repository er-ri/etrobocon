#!/usr/bin/env python3

import cv2
import time
import socket
import pickle
import struct
from etrobocon.unit import ETRobot

# Lable for saved camera capture and steering data
FILE_LABEL = int(time.time())

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(
    filename=f"storage/{FILE_LABEL}_picamera.avi",
    fourcc=fourcc,
    fps=20.0,
    frameSize=(640, 480),
)

# Socket connection for sending camera capture
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.45", 8485))


# Driving data recorder
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video
recorder = {
    "frame": [cap.get(cv2.CAP_PROP_POS_FRAMES)],
    "steer": [cap.get(cv2.CAP_PROP_POS_FRAMES)],
    "motor_count": [cap.get(cv2.CAP_PROP_POS_FRAMES)],
}

et = ETRobot()

while et.is_running == False:
    success, frame = cap.read()
    out.write(frame)

    # Get operation command(line follower or by Nvidia Model)
    # steer = model(section, frame)

    # Take the corresponding action
    # et.set_motor(power, steer)

    # Record driving data

    # Send the current camera's capture to the client
    # Not Implement: exit loop if connection lost
    ret, buffer = cv2.imencode(".png", frame)
    img_encoded = buffer.tobytes()
    data = pickle.dumps(img_encoded)
    client_socket.sendall(struct.pack("L", len(data)) + data)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

et.close_port()

with open(f"storage/{FILE_LABEL}_recorder.pickle", "wb") as file:
    pickle.dump(recorder, file)


cap.release()
out.release()
