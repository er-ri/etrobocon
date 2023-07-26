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

## Getting Started
*  Run the following command to launch the flask server

        flask run --host=0.0.0.0
