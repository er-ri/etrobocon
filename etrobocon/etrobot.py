import serial

class ETRobot(object):
    # Command Id
    MOVE_ID = 1
    STOP_ID = 9

    def __init__(self) -> None:
        self.serial = serial.Serial(
            port='/dev/ttyAMA1', baudrate=115200, timeout=2)

    def close_port(self) -> None:
        self.serial.close()

    def _send_command(self, command) -> None:
        self.serial.write(command)

    def move(self, angle: int) -> None:
        """Method to run lego spike.

        Args:
            angle: Steering wheel angle with the range of '0 ~ 180'

        Note:
            '0': turn left(the power of left wheel is 0)
            '180': turn right(the power of right wheel is 0)
        
        """
        id_byte = self.MOVE_ID.to_bytes(1, 'big') 
        parameter_byte = angle.to_bytes(1, 'big') 

        self._send_command(id_byte + parameter_byte)

    def stop(self) -> None:
        """Stop lego spike."""
        id_byte = self.STOP_ID.to_bytes(1, 'big')
        self._send_command(id_byte)
