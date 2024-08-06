import cv2
import numpy as np


def perform_edge_detection(image: np.ndarray) -> np.ndarray:
    """
    Convert to gray image, reduce noise(GaussianBlur) and then perform canny edge detection

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
        Visualization for a ROI from an image
        ---x--->
        |    -------------------------------------------
        |   |                                         |
        y   |    (x1, y1)      w                      |
        |   |      ------------------------           |
        v   |      |                      |           |
            |      |                      |           |
            |      |         ROI          | h         |
            |      |                      |           |
            |      |                      |           |
            |      |                      |           |
            |      ------------------------           |
            |                           (x2, y2)      |
            |                                         |
            -------------------------------------------

        To access the pixel located at x = 50, y = 20, pass the y-value first (the row number)
        followed by the x-value (the column number), resulting in image[y, x]
    """
    roi = image[y1:y2, x1:x2, :]
    new_image = cv2.resize(roi, new_size)

    return new_image


def draw_driving_info(
    gray: np.ndarray, info: dict, roi: tuple[int, int, int, int]
) -> np.ndarray:
    """
    Draw the current ETRobot driving information for the real-time inspection

    Args:
        gray: The current frame(converted to gray)
        info: Driving information

    Returns:
        The gray frame including ROI and the tracing point
    """
    mx, my = int(info["mx"]), int(info["my"])
    x1, y1, x2, y2 = roi

    gray = cv2.circle(gray, (mx + x1, my + y1), 3, (255, 255, 0), -1)  # Tracing point
    gray = cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 0, 255), 2)  # ROI

    for index, key in enumerate(info["text"]):
        gray = cv2.putText(
            gray,
            f"{key} : {info['text'][key]:.2f}",
            (50, 370 + index * 20),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
            cv2.LINE_4,
        )

    return gray


def extract_video_frames(video_path: str, frame_path: str, label: str) -> None:
    """
    Extract the video into frames and save those frames into a directory

    Args:
        video_path: Video file path
        frame_path: Path to save the extracted frames
        label: Frame file label
    """
    cap = cv2.VideoCapture(video_path)

    # Frame counter
    count = 0

    # Check whether the frame was successfully extracted
    success = 1

    while success:
        success, image = cap.read()

        if not success:
            break

        # Saves the frames with frame-count
        cv2.imwrite(f"{frame_path}{label}_frame%d.png" % count, image)
        count += 1
