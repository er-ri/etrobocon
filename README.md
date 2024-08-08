# ET Robot Contest
Project for ETRobo contest 2024

## Abstract
The project uses a LEGO Prime Hub and a Raspberry Pi to implement a line follower based on a CNN model that was proposed by Nvidia in 2016[1]. The CNN model predicts the offset to the center of the detected line that needs to be followed. The output power is calculated from the offset by a PID controller. 

## Folder Structure
```
.                        
└── etrobocon/
    ├── docs/                       # Documentation
    ├── spike/
    │   └── main.py                 # Program in LEGO Spike Prime for interacting with Raspberry Pi 
    ├── etrobocon/
    │   ├── data/
    │   │   ├── dataset.py          # Pytorch dataset definition
    │   │   └── preprocess.py       # Data preprocessing
    │   ├── models/
    │   │   └── nvidia.py           # Model definition
    │   ├── unit/
    │   │   └── etrobot.py          # Interface for controlling the ETRobot
    │   └── utils/
    │       ├── follower.py         # Line follower implementation
    │       ├── image.py            # Methods related to computer vision 
    │       └── pid.py              # PIDController implementation
    ├── storage/                    # Folder for storing training data and trained models
    ├── run.py                      # Starting ETRobot
    ├── collector.py                # For collecting training data
    ├── train.py                    # Script for performing the training task
    ├── receiver.py                 # Script for receiving Raspberry Pi camera (Running on Win/Unix)
    ├── requirements.txt            # Win/Unix dependencies for performing tasks of model training & data augmentation
    ├── requirements-reapi.txt      # Raspberry Pi dependencies for running the ETRobot
    ├── mkdocs.yml                  # Mkdocs configuration file
    ├── .readthedocs.yaml           # ReadtheDocs configuration file
    └── README.md                   # This file
```




## References
1. [End to End Learning for Self-Driving Cars](https://arxiv.org/abs/1604.07316)