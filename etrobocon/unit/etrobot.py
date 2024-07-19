import serial


class ETRobot(object):
    # Command Id
    MOTOR_ID = 1

    def __init__(self) -> None:
        self.serial_port = serial.Serial(
            port="/dev/ttyAMA1", baudrate=115200, timeout=2
        )
        self.section = 1
        self.terminated = False

    def _send_command(self, command) -> None:
        self.serial_port.write(command)

    def _receive_status(self, data):
        raise NotImplementedError

    def set_section(self) -> None:
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
