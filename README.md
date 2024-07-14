# ET Robot Contest
Repo for ETRobo contest 2024

## Project Structure
```
.                        
└── etrobocon/
    ├── docs/                       # Documentation
    ├── spike/
    │   └── main.py                 # Function used in LEGO Spike Prime Hub
    └── etrobocon/
        ├── operate/
        │   ├── manual.py
        │   └── auto.py
        └── etrobot.py              # Wrapped class for controlling ETRobot in Raspberry Pi
```

## ToDo
1. Data collection & labeling
2. Data preparation(augumentation, balancing, etc.)
3. Imitation learning
4. Reinforcement learning environment(gymnasium) 
5. Model training


## Getting Started
*  Run the following command to launch the flask server

        flask run --host=0.0.0.0
