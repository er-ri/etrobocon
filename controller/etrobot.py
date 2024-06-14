import serial

class ETRobot(object):

    def __init__(self) -> None:
        self.serial = serial.Serial(
            port='A', baudrate=115200, timeout=2)

    def _send_command(self, command) -> None:
        self.serial.write(command)