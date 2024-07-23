import time
import serial
import threading

class ETRobot(object):

    # Command ID
    # Values should be consistent with (`spike/main.py`) the script in LEGO Spike Prime
    COMMAND_MOTOR_ID = 1
    COMMAND_ARM_ID = 2

    def __init__(self) -> None:
        self._serial_port = serial.Serial(
            port="/dev/ttyAMA1", baudrate=115200, timeout=2
        )
        
        self.color_sensor = None
        self.motor_count = None
        self.is_running = True

        self.thread = threading.Thread(target=self._update_status)
        self.thread.start()

    def _send_command(self, command) -> None:
        self._serial_port.write(command)

    def _update_status(self):
        """Update ETRobot motor and sensor status by the recieved data with GPIO port
        
        Note:
            Update rate should be less than the rate of sending sensor data in LEGO Prime Hub(`0.05`)
        """
        self._serial_port.flush()

        while self.is_running:
            status_data = self._serial_port.read(3)

            if status_data != b"":
                color_sensor = int.from_bytes(status_data[0:1], "big")
                motor_count = int.from_bytes(status_data[1:3], "big")
                self.color_sensor = color_sensor
                self.motor_count = motor_count
            time.sleep(0.03)    # Value should be less than `0.05`

    def set_motor_power(self, left_power: int, right_power: int) -> None:
        """Method to set the ETRobot motor's power

        Args:
            left_power: Left moter power(0~100)
            right_power: Right moter power(0~100)
        """
        id_byte = self.COMMAND_MOTOR_ID.to_bytes(1, "big")
        parameter1_byte = left_power.to_bytes(1, "big")
        parameter2_byte = right_power.to_bytes(1, "big")

        command = id_byte + parameter1_byte + parameter2_byte
        
        self._send_command(command)

    def stop(self) -> None:
        self.is_running = False
        self.set_motor_power(0, 0)
        self.thread.join()
        self._serial_port.close()
