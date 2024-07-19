#!/usr/bin/env python3

import cv2
import socket
import pickle
import struct
from etrobocon.unit import ETRobot

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(
    filename="data/output.avi", fourcc=fourcc, fps=20.0, frameSize=(640, 480)
)

# Socket connection for sending camera capture
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.45", 8485))


et = ETRobot()

while et.terminated == False:
    success, frame = cap.read()
    out.write(frame)

    # Set section(by color sensor)

    # Get operation command(line follower or by Nvidia Model)
    # steering = model(section, frame)

    # Take the corresponding action
    # et.set_motor(power, steering)

    # Send the current camera's capture to the client
    ret, buffer = cv2.imencode(".png", frame)
    img_encoded = buffer.tobytes()
    data = pickle.dumps(img_encoded)
    client_socket.sendall(struct.pack("L", len(data)) + data)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

et.close_port()

cap.release()
out.release()
