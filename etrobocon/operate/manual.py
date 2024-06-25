import json
from etrobocon import ETRobot


def control_spike_car(command: str) -> None:
    """Interpret user keyboard input to etrobot commands.

    Args:
        command: raw command string in json style.

    Note:
        | Key | Value | Description |
        | --- | --- | --- |
        | "D" | 0 | Full Left |
        | "F" | 45 | Left |
        | Space | 90 | Straight |
        | "J" | 135 | Right | 
        | "K" | 180 | FUll Right |

    """
    command = json.loads(command)

    match command['code']:
        case "KeyD":
            ETRobot.move(0)
        case "KeyF":
            ETRobot.move(45)
        case "Space":
            ETRobot.move(90)
        case "KeyJ":
            ETRobot.move(135)
        case "KeyK":
            ETRobot.move(180)
        case "KeyB":
            ETRobot.stop()
        case _:
            pass