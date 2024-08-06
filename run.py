#!/usr/bin/env python3
import cv2
import time
import socket
import pickle
import struct
from etrobocon.unit import ETRobot
from etrobocon.utils import steer_by_camera, draw_driving_info, PIDController
from etrobocon.data import REGION_OF_INTEREST

# User defined constants
FILE_LABEL = time.strftime(
    "%Y%m%d%H%M%S", time.localtime()
)  # Label for saved camera capture and steering data
SPECIFIED_FPS = 20  # PICamera fps
DELTA_TIME = 1 / SPECIFIED_FPS  # Interval between two frames (used by PID controller)
POWER = 35  # Base motor power
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


# Driving data recorder
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video

# Socket connection for sending camera capture
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP_ADDRESS, 8485))


def run_one_frame(et: ETRobot, pid: PIDController, delta_time: float) -> None:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return False

    out.write(frame)

    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

    roi = gray[y1:y2, x1:x2]

    distance, info = steer_by_camera(roi=roi)

    steer = pid.update(distance, delta_time=delta_time)

    left_power = POWER - steer
    right_power = POWER + steer

    et.set_motor_power(left_power=left_power, right_power=right_power)

    # Draw driving info for inspection
    info["text"] = {
        "distance": distance,
        "steer": steer,
        "left_power": left_power,
        "right_power": right_power,
    }
    gray = draw_driving_info(gray, info, (x1, y1, x2, y2))

    # Send camera capture
    ret, buffer = cv2.imencode(".png", gray)
    img_encoded = buffer.tobytes()
    data = pickle.dumps(img_encoded)
    client_socket.sendall(struct.pack("L", len(data)) + data)


def main():
    pid = PIDController(Kp=0.1, Ki=0.001, kd=0, setpoint=0, output_limits=(-35, 35))
    et = ETRobot()

    # Start
    run_one_frame(et=et, pid=pid, delta_time=0)

    while et.is_running == True:
        ret = run_one_frame(et=et, pid=pid, delta_time=DELTA_TIME)

        if cv2.waitKey(0) & 0xFF == ord("q") or not ret:
            break

    et.stop()

    cap.release()
    out.release()


if __name__ == "__main__":
    main()
