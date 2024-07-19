import cv2
import numpy as np


def perform_edge_detection(image: np.ndarray) -> np.ndarray:
    """Convert to gray image, reduce noise(GaussianBlur) and then perform canny edge detection

    Args:
        image: Original input image

    Returns:
        The new image contains edge info
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)

    return canny


def extract_roi_and_resize(
    image: np.ndarray,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    new_size: tuple = (200, 66),
) -> np.ndarray:
    """Extract the Region-Of-Interest(ROI)

    Args:
        x1: Top-left vertex(x1)
        y1: Top-left vertex(y1)
        x2: Bottom-right vertex(x2)
        y2: Bottom-right vertex(y2)
        new_size: Default value (200, 60) using for Nvidia model

    Returns:
        Region-Of-Interest area with defined size

    !!! Note
        Visualization for selecting a ROI from an image

            -------------------------------------------
            |                                         |
            |    (x1, y1)      w                      |
            |      ------------------------           |
            |      |                      |           |
            |      |                      |           |
            |      |         ROI          | h         |
            |      |                      |           |
            |      |                      |           |
            |      |                      |           |
            |      ------------------------           |
            |                           (x2, y2)      |
            |                                         |
            -------------------------------------------
    """
    roi = image[y1:y2, x1:x2, :]
    new_image = cv2.resize(roi, new_size)

    return new_image


def draw_driving_info():
    """Draw the current ETRobot driving information for real-time inspection"""
    raise NotImplementedError
