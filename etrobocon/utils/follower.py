"""Line follower

The module contains line follower implementation of camera based and colorsensor based, 
which are used for training data collection for the model. By sending the input data
such as camera image or sensor status, the function will return the steering angle. 
"""

import cv2
import math
import numpy as np


def steer_by_camera(image: np.ndarray) -> tuple[float, dict]:
    """Function used for line follower by calculating its steering angle for the given image

    Args:
        image: input image from raspiberry pi camera

    Returns:
        steering: wheel steering angle
        info: driving information for inspecition
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    max_contour = max(contours, key=cv2.contourArea)

    [vx, vy, x, y] = cv2.fitLine(max_contour, cv2.DIST_L2, 0, 0.01, 0.01)

    line_angle = math.atan2(vy[0], vx[0])
    line_angle += math.pi / 2 if line_angle < 0 else -math.pi / 2

    steering = math.degrees(line_angle)

    return steering, {vx[0], vy[0], x[0], y[0]}


def follow_line_by_sensor():
    raise NotImplementedError
