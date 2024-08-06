"""
Line Follower

This module contains implementations of line-following algorithms using camera-based 
and color sensor-based methods. These implementations are used for training data 
collection for a model. By sending input data such as a camera image or sensor status, 
the functions return the necessary adjustments.

Functions:
    steer_by_camera(roi: np.ndarray) -> tuple[float, dict]:
        Calculates the steering adjustment based on the difference between the 
        center of the Region of Interest (ROI) and the centroid of the largest contour 
        in the x-coordinate.

    steer_by_reflection(reflection: int, threshold: int) -> int:
        Determines the steering adjustment based on light reflectivity detected by 
        a color sensor, guiding the robot to follow the edge of a line.
"""

import cv2
import numpy as np


def steer_by_camera(roi: np.ndarray) -> tuple[float, dict]:
    """Calculates the steering adjustment for a LEGO line follower by determining the
    difference between the center of the Region of Interest (ROI) and the centroid
    of the largest contour in the x-coordinate.

    Args:
        roi (np.ndarray): ROI, a gray image is expected.

    Returns:
        distance (float): Distance between the center of the ROI and the centroid in x coordinates.
        info (dict): Driving information for inspection, including the largest contour and its centroid coordinates.
    """
    blur = cv2.GaussianBlur(roi, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    max_contour = max(contours, key=cv2.contourArea)

    mu = cv2.moments(max_contour)
    # Add 1e-5 to avoid division by zero
    mx = mu["m10"] / (mu["m00"] + 1e-5)
    my = mu["m01"] / (mu["m00"] + 1e-5)

    # Distance between ROI center and the centroid in x coordinates
    distance = mx - (roi.shape[1] / 2)

    return distance, {"max_contour": max_contour, "mx": mx, "my": my}


def steer_by_reflection(reflection: int, threshold: int) -> int:
    """Determines the steering adjustment based on light reflectivity detected by a color sensor.
    The robot follows the edge of a line, turning one way when it detects more light reflectivity
    (whitish color) and the other way when it detects less light reflectivity (darkish color).

    Args:
        reflection (int): Light reflection value (white: 100, black: 0).
        threshold (int): The value to trigger the robot's turning.

    Returns:
        reflection_diff (int): The difference between the detected reflection value and the threshold.
    """
    reflection_diff = reflection - threshold
    return reflection_diff
