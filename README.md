# ET Robot Contest
Project for ETRobo contest 2024

* Official Github: https://github.com/ETrobocon 



PID Controller Tuning: Ziegler–Nichols method

## Project Structure
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
    │   │   └── nvidia.py           # "End to End Learning for Self-Driving Cars" model definition
    │   ├── unit/
    │   │   └── etrobot.py          # Interface for controlling the ETRobot
    │   └── utils/
    │       ├── follower.py         # Line follower implementation
    │       ├── image.py            # Methods related to computer vision 
    │       └── pid.py              # PIDController implementation
    ├── storage/                    # Folder for storing training data and trained models
    ├── run.py                      # Entry point for starting the robot
    ├── train.py                    # Script for performing the training task
    ├── receiver.py                 # Script for receiving Raspberry Pi camera (Running on Win/Unix)
    ├── requirements.txt            # Win/Unix dependencies for performing tasks of model training & data augmentation
    ├── requirements-reapi.txt      # Raspberry Pi dependencies for running the ETRobot
    ├── mkdocs.yml                  # Mkdocs configuration file
    ├── .readthedocs.yaml           # ReadtheDocs configuration file
    └── README.md                   # This file
```



