import serial
import threading


class ETRobot(object):
    # Command Id
    MOTOR_ID = 1

    def __init__(self) -> None:
        self.serial_port = serial.Serial(
            port="/dev/ttyAMA1", baudrate=115200, timeout=2
        )
        self.is_running = True

    def _send_command(self, command) -> None:
        self.serial_port.write(command)

    def update_status(self):
        """Update ETRobot motor and sensor status from recieved data from GPIO port"""

        # Read and update ETRobot status

        raise NotImplementedError

    def set_motor_power(self, power: int, steering: int) -> None:
        """Method to set the ETRobot motor's power

        Args:
            power: Moter power(0~100)
            steering: Steering wheel angle(-90 ~ 90)
        """
        id_byte = self.MOTOR_ID.to_bytes(1, "big")
        parameter1_byte = power.to_bytes(1, "big")
        parameter2_byte = steering.to_bytes(1, "big")

        self._send_command(id_byte + parameter1_byte + parameter2_byte)

    def get_color_sensor_status():
        raise NotImplementedError

    def get_ultrasonic_sensor_status():
        raise NotImplementedError

    def close_port(self) -> None:
        self.serial_port.close()
