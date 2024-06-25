import serial

class ETRobot(object):
    # Command Id
    MOVE_ID = 1
    STOP_ID = 9

    serial_port = serial.Serial(port='/dev/ttyAMA1', baudrate=115200, timeout=2)

    @classmethod
    def close_port(cls) -> None:
        cls.serial_port.close()

    @classmethod
    def _send_command(cls, command) -> None:
        cls.serial.write(command)

    @classmethod
    def move(cls, angle: int) -> None:
        """Method to run lego spike.

        Args:
            angle: Steering wheel angle with the range of '0 ~ 180'

        Note:
            '0': turn left(the power of left wheel is 0)
            '180': turn right(the power of right wheel is 0)
        
        """
        id_byte = cls.MOVE_ID.to_bytes(1, 'big') 
        parameter_byte = angle.to_bytes(1, 'big') 

        cls._send_command(id_byte + parameter_byte)

    @classmethod
    def stop(cls) -> None:
        """Stop lego spike."""
        id_byte = cls.STOP_ID.to_bytes(1, 'big')
        cls._send_command(id_byte)
