"""
This module provides functions for labeling and balancing datasets of image frames.

Functions:
    label_dataset(path_pattern: str, output_csv: str, roi: tuple[int, int, int, int]) -> pd.DataFrame:
        Labels all the frame files in the provided path pattern and saves the 'frame-distance' pairs to a CSV file.
        
    balance_dataset(df: pd.DataFrame, col_name: str, max_samples: int, num_bins: int) -> pd.DataFrame:
        Balances the dataset by limiting the number of samples in each bin of a specified column.
"""

import cv2
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.utils import shuffle
from etrobocon.utils import steer_by_camera


def label_dataset(
    path_pattern: str, output_csv: str, roi: tuple[int, int, int, int]
) -> pd.DataFrame:
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

    x1, y1, x2, y2 = roi

    # Get list of all file paths matching the pattern
    file_paths = glob.glob(path_pattern)
    data = list()

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


def balance_dataset(
    df: pd.DataFrame, col_name: str, max_samples: int, num_bins: int
) -> pd.DataFrame:
    """
    Balances the dataset by limiting the number of samples in each bin of a specified column.

    This function creates a histogram of the specified column and ensures that no bin has more than
    `max_samples` samples. If a bin exceeds this limit, excess samples are randomly removed to balance
    the dataset.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be balanced.
        col_name (str): The name of the column to be used for creating bins.
        max_samples (int): The maximum number of samples allowed per bin.
        num_bins (int): The number of bins to divide the column into.

    Returns:
        pd.DataFrame: A DataFrame with the dataset balanced according to the specified column and bin limits.
    """

    hist, bins = np.histogram(df[col_name], num_bins)

    # Initialize an empty list to store indices to remove
    remove_list = list()

    # Iterate over each bin
    for i in range(num_bins):
        # Get the indices of the samples in the current bin
        bin_indices = df[
            (df[col_name] >= bins[i]) & (df[col_name] <= bins[i + 1])
        ].index.tolist()

        # Shuffle the indices
        bin_indices = shuffle(bin_indices)

        # If the number of samples in the bin exceeds the limit, add the excess to the remove list
        if len(bin_indices) > max_samples:
            remove_list.extend(bin_indices[max_samples:])

    # Drop the rows from the DataFrame
    df = df.drop(remove_list)
    return df
