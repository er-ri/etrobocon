import time
import pickle
import serial


class ETRobot(object):
    # Command Id
    MOVE_ID = 1
    STOP_ID = 9

    def __init__(self) -> None:
        self.serial_port = serial.Serial(
            port="/dev/ttyAMA1", baudrate=115200, timeout=2
        )
        self.section = 1
        self.last_indicator = None
        self.recorder = {"command": [], "time": []}
        self.terminated = False

    def _send_command(self, command) -> None:
        self.recorder["command"].append(command)
        self.recorder["time"].append(time.time())
        self.serial_port.write(command)

    def _receive_status(self, data):
        pass

    def set_section(self, indicator) -> None:
        if indicator == "WHITE" and self.last_indicator == "BLUE":
            self.section += 1

        self.last_indicator = indicator

    def move(self, angle: int) -> None:
        """Method to run lego spike.

        Args:
            angle: Steering wheel angle with the range of '0 ~ 180'

        Note:
            '0': turn left(the power of left wheel is 0)
            '180': turn right(the power of right wheel is 0)

        """
        id_byte = self.MOVE_ID.to_bytes(1, "big")
        parameter_byte = angle.to_bytes(1, "big")

        self._send_command(id_byte + parameter_byte)

    def stop(self) -> None:
        id_byte = self.STOP_ID.to_bytes(1, "big")
        self._send_command(id_byte)
        self.terminated = True

    def close_port(self) -> None:
        self.serial_port.close()

    def save_record(self) -> None:
        with open("data/command.pickle", "wb") as file:
            pickle.dump(self.recorder, file)
