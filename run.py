#!/usr/bin/env python3
import cv2
import time
import socket
import pickle
import struct
from etrobocon.unit import ETRobot
from etrobocon.utils import steer_by_camera, draw_driving_info, PIDController

# User defined constants
FILE_LABEL = time.strftime(
    "%Y%m%d%H%M%S", time.localtime()
)  # Label for saved camera capture and steering data
SPECIFIED_FPS = 20  # PICamera fps
BASE_POWER = 50  # Base motor power
x1, y1, x2, y2 = 100, 200, 540, 300  # Region of Interest
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


# Driving data recorder
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video

# Socket connection for sending camera capture
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP_ADDRESS, 8485))


def main():
    pid = PIDController(
        Kp=0.1, Ki=0.001, Kd=0, setpoint=0, output_limits=(-BASE_POWER, BASE_POWER)
    )
    et = ETRobot()

    while et.is_running == True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        out.write(frame)

        gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

        roi = gray[y1:y2, x1:x2]

        mx, my, _ = steer_by_camera(roi=roi)
        # Distance between ROI center and the centroid in x coordinates
        distance = mx - (roi.shape[1] / 2)

        # Steering angle range: -1 ~ 1 (1: trun right; -1: turn left)
        steer = pid.update(distance) / BASE_POWER
        left_power = BASE_POWER * (1 + steer) if steer <= 0 else BASE_POWER
        right_power = BASE_POWER * (1 - steer) if steer >= 0 else BASE_POWER

        et.set_motor_power(left_power=int(left_power), right_power=int(right_power))

        # Draw driving information for the real-time inspection
        info = dict()
        info["mx"], info["my"] = mx, my
        info["text"] = {
            "distance": distance,
            "steer": steer,
            "left_power": left_power,
            "right_power": right_power,
        }
        gray = draw_driving_info(gray, info, (x1, y1, x2, y2))

        # Send camera capture to pc
        ret, buffer = cv2.imencode(".png", gray)
        img_encoded = buffer.tobytes()
        data = pickle.dumps(img_encoded)
        client_socket.sendall(struct.pack("L", len(data)) + data)

        if cv2.waitKey(1) & 0xFF == ord("q") or not ret:
            break

    et.stop()

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
