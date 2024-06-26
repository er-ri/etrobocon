# LEGO type:standard slot:2 autostart
"""Main controlling program for LEGO Spike Prime Hub Car 

The program was running on a LEGO Spike Prime Hub that controlled the 
vehicle's behavior by receiving commands that were sent by the Raspberry Pi 
through GPIO. The micropython package `uasyncio` has been implemented for 
asynchronous communication. 

"""
import gc
import hub
import time
import uasyncio

MAX_IDEL_TIME = 10000    # Maximum idel time, unit: millisecond
PWM_RATIO = 0.3         # Motor power = 90 * PWM_RATIO

PORT_MAP = {
    "motor_arm": "A",
    "motor_right": "B",
    "motor_left": "E",
    "color_sensor": "C",
    "ultrasonic_sensor": "F",
    "serial_port": "D",
}


class SpikeCar(object):
    """LEGO Spike Prime Hub based Car

    Class for controlling all the devices in the Spike car by receiving 
    commands from Raspberry Pi. Every command is made up of 2 bytes, the 
    first byte indicates the command id while the second byte represents 
    the corresponding parameters as shown below. 

    | Device | Command Id | Parameters |
    | SteeringWheel | 0 | 0~180 |

    """

    def __init__(self) -> None:
        # Initialization
        hub.display.show(hub.Image.ALL_CLOCKS, delay=400, clear=True, wait=False, loop=True, fade=0)
        hub.motion.align_to_model(hub.TOP, hub.FRONT)   # GYRO, orientation
        hub.motion.yaw_pitch_roll(0)                    # yaw, pitch and roll

        # Set ports
        self.motor_arm = getattr(hub.port, PORT_MAP["motor_arm"]).motor
        self.motor_right = getattr(hub.port, PORT_MAP["motor_right"]).motor
        self.motor_left = getattr(hub.port, PORT_MAP["motor_left"]).motor
        self.color_sensor = getattr(hub.port, PORT_MAP["color_sensor"]).device
        self.ultrasonic_sensor = getattr(hub.port, PORT_MAP["ultrasonic_sensor"]).device
        self.serial_port = getattr(hub.port, PORT_MAP['serial_port'])

        # The serial port will operates as a raw full duplex logic level(data can be transmitted in both directions send/receive)
        self.serial_port.mode(hub.port.MODE_FULL_DUPLEX)
        # Setup the serial port(take 1 second), and transferring a maximum of 115200 bits per second.
        time.sleep(1)
        self.serial_port.baud(115200)

        # Clear serial port buffer(By reading all bytes)
        while self.serial_port.read(100) != b'':
            continue

        # Millisecond counter for record the latest command executed time
        self.command_counter = time.ticks_ms()

        image = hub.Image.SMILE
        hub.display.show(image)


    def read_command(self):
        raw_bytes = self.serial_port.read(2)
        command_id = None
        command_parameter = None

        if raw_bytes != b'':
            command_id = int.from_bytes(raw_bytes[0:1], "big")
            command_parameter = int.from_bytes(raw_bytes[1:2], "big")
            self.command_counter = time.ticks_ms()

        return command_id, command_parameter


    def execute_command(self, command_id, command_parameter):
        if command_id == 1:
            self._move(command_parameter)
        elif command_id == 2:
            print("Command 2 received with the parameter of {}".format(command_parameter))
        elif command_id == 9:
            self.stop_spike()
        else:
            print("Unknow command received, id={}; parameter={}".format(command_id, command_parameter))


    def _move(self, angle):
        """Method to control the steering wheel angle.

        Args:
            angle: Steering wheel angle with the range of '0 ~ 180'

        Note:
            '0' means turn left while '180' means turn right.
        """
        if angle > 180:
            return
        
        self.command_counter = time.ticks_ms()

        left_wheel_speed = min(angle, 90)
        right_wheel_speed = 90 if angle < 90 else 180 - angle

        self.motor_left.pwm(int(left_wheel_speed * PWM_RATIO))
        self.motor_right.pwm(-int(right_wheel_speed * PWM_RATIO))


    def stop_spike(self):
        self.motor_left.pwm(0)
        self.motor_right.pwm(0)


async def receiver():

    while True:
        command_id, command_parameter = spike_car.read_command()
        if command_id != None:
            spike_car.execute_command(command_id, command_parameter)

        if time.ticks_ms() - spike_car.command_counter > MAX_IDEL_TIME:
            raise SystemExit("Maximum idle time reached, terminate lego spike.")

        await uasyncio.sleep(0)


async def main_task():
    tasks = list()
    task = uasyncio.create_task(receiver())
    tasks.append(task)
    await uasyncio.sleep(1*60)     # Max running time, unit: seconds

    # Cancel all tasks.
    for task in tasks:
        task.cancel()

# triggers a garbage collection cycle
gc.collect()
print("Started")

try:
    spike_car = SpikeCar()
    uasyncio.run(main_task())
except SystemExit as se:
    print(se)

hub.display.show(hub.Image.ASLEEP)
print("Ended")
