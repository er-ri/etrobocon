"""
Module for data preprocessing including data balancing, data labelling and visualization.
"""

import cv2
import glob
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from etrobocon.utils import steer_by_camera

# Define the Region of Interest (ROI) coordinates
REGION_OF_INTEREST = (100, 200, 540, 300)


def label_dataset(path_pattern: str, output_csv: str) -> pd.DataFrame:
    """
    Labels all the frame files in the provided path pattern and saves the 'frame-distance' pairs to a CSV file.

    Args:
        path_pattern (str): Pathname pattern such as "./frames/*.png".
        output_csv (str): Path to the output CSV file.

    Returns:
        pd.DataFrame: DataFrame containing pairs of frame file paths and their corresponding distances.

    Note:
        Read the csv file to DataFrame by `df = pd.read_csv('./label.csv')`
    """

    x1, y1, x2, y2 = REGION_OF_INTEREST

    # Get list of all file paths matching the pattern
    file_paths = glob.glob(path_pattern)
    data = []

    # Process each file
    for file_path in tqdm(file_paths):
        frame = cv2.imread(file_path)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray_frame[y1:y2, x1:x2]
        distance, _ = steer_by_camera(roi=roi)
        data.append({"file_path": file_path, "distance": distance})

    # Create DataFrame from collected data
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv(output_csv, index=False)

    return df


def visualize_distribution(df: pd.DataFrame, col_name: str, bins: int) -> None:

    plt.hist(df[col_name], bins=bins, color="skyblue", edgecolor="black")

    # Adding labels and title
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title("Data Distribution")

    # Display the plot
    plt.show()
