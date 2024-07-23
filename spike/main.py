# LEGO type:standard slot:2 autostart
"""Main controlling program for LEGO Spike Prime Hub 

The program was running on a LEGO Spike Prime Hub that controlled the 
ETRobot's behavior by receiving commands that were sent by the Raspberry Pi 
through GPIO. The asynchronous communication with Raspberry Pi was 
implemented by the micropython package `uasyncio`.  

Appendix:

**Color Sensor**

The Color Sensor can give the following data:

| Mode | Output | Description |
| --- | --- | --- |
| Color(2) | -1 ~ 10 | Each number represents a detected color |
| Reflected(3) | 0 ~ 100 | 0% = no reflection, 100% = very reflective |
| Ambient(2) | 0 ~ 100 | 0% = dark, 100% = bright |

Set the mode and retrieve the sensor data in the following way

```python
# Set mode
color_sensor.mode(0)
# Retrieve its detected value
ret = color_sensor.get()
```

Ref: https://ev3-help-online.api.education.lego.com/Retail/en-us/page.html?Path=editor%2FUsingSensors_Color.html

"""
import gc
import hub
import time
import uasyncio

MAX_IDEL_TIME = 15000  # Maximum idel time, unit: millisecond

# Command ID list
COMMAND_MOTOR_ID = 1
COMMAND_ARM_ID = 2

PORT_MAP = {
    "motor_arm": "C",
    "motor_right": "B",
    "motor_left": "E",
    "color_sensor": "A",
    "ultrasonic_sensor": "F",
    "serial_port": "D",
}


class SpikeCar(object):
    """LEGO Spike Prime Hub based Car

    Class for controlling all the devices in the Spike car by receiving
    commands from Raspberry Pi. Every command is made up of 2 bytes, the
    first byte indicates the command id while the second byte represents
    the corresponding parameters as shown below.

    | Device | Command Id | Parameter1 | Parameter2 |
    | Motor | 0 | Power: 0~180 | Steering: -90 ~ 90  |

    """

    def __init__(self) -> None:
        # Initialization
        hub.display.show(
            hub.Image.ALL_CLOCKS, delay=400, clear=True, wait=False, loop=True, fade=0
        )
        hub.motion.align_to_model(hub.TOP, hub.FRONT)  # GYRO, orientation
        hub.motion.yaw_pitch_roll(0)  # yaw, pitch and roll

        # Set ports
        self.motor_arm = getattr(hub.port, PORT_MAP["motor_arm"]).motor
        self.motor_right = getattr(hub.port, PORT_MAP["motor_right"]).motor
        self.motor_left = getattr(hub.port, PORT_MAP["motor_left"]).motor
        self.color_sensor = getattr(hub.port, PORT_MAP["color_sensor"]).device
        self.ultrasonic_sensor = getattr(hub.port, PORT_MAP["ultrasonic_sensor"]).device
        self.serial_port = getattr(hub.port, PORT_MAP["serial_port"])

        # The serial port will operates as a raw full duplex logic level(data can be transmitted in both directions send/receive)
        self.serial_port.mode(hub.port.MODE_FULL_DUPLEX)
        # Setup the serial port(take 1 second), and transferring a maximum of 115200 bits per second.
        time.sleep(1)
        self.serial_port.baud(115200)

        # Initialization & Set motors mode to measure its relative position on boot
        self.motor_left.mode([(2, 0)])
        self.motor_right.mode([(2, 0)])
        self.motor_left.preset(0)
        self.motor_right.preset(0)

        # Set color sensor to reflection mode
        self.color_sensor.mode(1)

        # Clear serial port buffer
        while self.serial_port.read(100) != b"":
            continue

        # Millisecond counter for record the latest command executed time, maximum idle time
        self.command_counter = time.ticks_ms()

        hub.display.show(hub.Image.SMILE)

    def read_command(self):
        raw_bytes = self.serial_port.read(3)
        command_id = None
        command_parameter1 = None
        command_parameter2 = None

        if raw_bytes != b"":
            command_id = int.from_bytes(raw_bytes[0:1], "big")
            command_parameter1 = int.from_bytes(raw_bytes[1:2], "big")
            command_parameter2 = int.from_bytes(raw_bytes[2:3], "big")
            self.command_counter = time.ticks_ms()

        return command_id, command_parameter1, command_parameter2

    def send_status(self):
        """Send the ETRtobot's status, including motor and sensor data.
        Data are sent by GPIO serial port

        Note:
            Sent data are following the below format

            122

            Where '1' is the reflection(color sensor), '2' is the motor count
        """
        reflection = self.color_sensor.get()
        motor_count = self.motor_left.get()
        
        # if motor_count != 0:
        #     print(motor_count)

        reflection_byte = reflection[0].to_bytes(1, "big")
        motor_count_byte = motor_count[0].to_bytes(2, "big")

        status_data = reflection_byte + motor_count_byte
        self.serial_port.write(status_data)

    def execute_command(self, command_id, command_parameter1, command_parameter2):
  
        print(
            "Command received, id={}; parameter1={}; parameter2={}".format(
                command_id, command_parameter1, command_parameter2
            )
        )
        
        if command_id == COMMAND_MOTOR_ID:
            self._set_motor_power(command_parameter1, command_parameter2)
        elif command_id == COMMAND_ARM_ID:
            pass
        else:
            pass

    def _set_motor_power(self, left_power: int, right_power: int) -> None:
        """Method to control the steering wheel angle.

        Args:
            left_power: Left wheel power(0~100)
            right_power: Right wheel power(0~100)
        """
        self.command_counter = time.ticks_ms()

        self.motor_left.pwm(int(left_power))
        self.motor_right.pwm(-int(right_power))


async def receiver():
    while True:
        command_id, command_parameter1, command_parameter2 = spike_car.read_command()
        if command_id != None:
            spike_car.execute_command(
                command_id, command_parameter1, command_parameter2
            )

        if time.ticks_ms() - spike_car.command_counter > MAX_IDEL_TIME:
            raise SystemExit("Maximum idle time reached, terminate lego spike.")

        await uasyncio.sleep(0)


async def sender():
    while True:
        spike_car.send_status()
        await uasyncio.sleep(0.05)      # Send data 20 times per second


async def main_task():
    tasks = list()

    receiver_task = uasyncio.create_task(receiver())
    tasks.append(receiver_task)
    sender_task = uasyncio.create_task(sender())
    tasks.append(sender_task)

    await uasyncio.sleep(1 * 60)  # Max running time, unit: seconds

    # Cancel all tasks.
    for task in tasks:
        task.cancel()


# triggers a garbage collection cycle
gc.collect()

print("Starting LEGO Prime Hub..")

try:
    spike_car = SpikeCar()
    uasyncio.run(main_task())
except SystemExit as e:
    print(e)

hub.display.show(hub.Image.ASLEEP)

print("Completed")