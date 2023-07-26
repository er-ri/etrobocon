from etrobocon import ETRobot


def control_spike_car(command: dict) -> None:
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
    if command['code'] == "KeyD":
        ETRobot.move(0)
    elif command['code'] == "KeyF":
        ETRobot.move(45)
    elif command['code']== "Space":
        ETRobot.move(90)
    elif command['code'] == "KeyJ":
        ETRobot.move(135)
    elif command['code'] == "KeyK":
        ETRobot.move(180)
    elif command['code'] == "KeyB":
        ETRobot.stop()
    elif command['code'] == "KeyT":
        ETRobot.save_record()
    else:
        pass