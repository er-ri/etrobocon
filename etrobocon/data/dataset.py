"""Pytorch dataset definition including Data Augmentation
"""

import cv2
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import Dataset

transform = A.Compose(
    [
        A.ShiftScaleRotate(
            shift_limit=0.03,
            scale_limit=0.03,
            rotate_limit=0,
            border_mode=cv2.BORDER_CONSTANT,
            p=0.5,
        ),
        A.RandomBrightnessContrast(p=0.5),
    ]
)

# Define the method separately, for the steering angle(label) also need to be flipped if the transformer was applied
flip_transform = A.ReplayCompose(
    [
        A.HorizontalFlip(p=0.5),
        ToTensorV2(),
    ]
)


class DrivingRecordDataset(Dataset):
    """Pytorch dataset together with augmentation methods

    1. `ShiftScaleRotate`
    2. `RandomBrightnessContrast`
    3. `HorizontalFlip`
    """

    def __init__(self, image_paths, steerings, transform=None, flip_transform=None):
        self.image_paths = image_paths
        self.steerings = steerings
        self.transform = transform
        self.flip_transform = flip_transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = cv2.imread(image_path)
        image = image[60:135, :, :]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.resize(image, (200, 66))
        image = image / 255
        label = self.steerings[idx]

        if self.transform is not None:
            image = self.transform(image=image)["image"]

        if self.flip_transform is not None:
            transformed_image = self.flip_transform(image=image)
            image = transformed_image["image"]

            # Reverse steering angle if the horizontal flip has been performed
            if transformed_image["replay"]["transforms"][0]["applied"] is True:
                label = -label

        # Module `Conv2d` supports up to `TensorFloat32`
        image = image.to(torch.float32)
        label = torch.tensor(label, dtype=torch.float32).unsqueeze(-1)

        return image, label
