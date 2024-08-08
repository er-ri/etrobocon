#!/usr/bin/env python3
"""Script for collecting training data"""
import cv2
import time
import socket
import pickle
import struct
from etrobocon.utils import steer_by_camera, draw_driving_info
from etrobocon.data import REGION_OF_INTEREST


# User defined constants
FILE_LABEL = time.strftime(
    "%Y%m%d%H%M%S", time.localtime()
)  # Label for saved camera capture and steering data
SPECIFIED_FPS = 20  # PICamera fps
x1, y1, x2, y2 = REGION_OF_INTEREST  # Region of Interest
HOST_IP_ADDRESS = (
    "192.168.137.1"  # The destination IP that the Raspberry Pi will send to
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


# Socket connection for sending camera capture
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP_ADDRESS, 8485))


def main():

    # Start
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return False

        out.write(frame)

        gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

        roi = gray[y1:y2, x1:x2]

        mx, my, _ = steer_by_camera(roi=roi)

        # Draw driving info for inspection
        info = dict()
        info["mx"], info["my"] = mx, my
        gray = draw_driving_info(gray, info, (x1, y1, x2, y2))

        # Send camera capture
        ret, buffer = cv2.imencode(".png", gray)
        img_encoded = buffer.tobytes()
        data = pickle.dumps(img_encoded)
        client_socket.sendall(struct.pack("L", len(data)) + data)

        if cv2.waitKey(1) & 0xFF == ord("q") or not ret:
            break

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
