# LEGO type:standard slot:2 autostart
import gc
import hub
import uasyncio

MOTER_POWER = 10

PORT_MAP = {
    "motor_A": "A",
    "motor_B": "B",
    "motor_C": "E",
    "color_sensor": "C",
    "ultrasonic_sensor": "F",
    "serial_port": "D",
}


class SpikeCar(object):

    def __init__(self) -> None:
        # Initialization
        hub.display.show(hub.Image.ALL_CLOCKS, delay=400, clear=True, wait=False, loop=True, fade=0)
        hub.motion.align_to_model(hub.TOP, hub.FRONT)   # GYRO, orientation
        hub.motion.yaw_pitch_roll(0)                    # yaw, pitch and roll

        # Set ports
        self.motor_A = getattr(hub.port, PORT_MAP["motor_A"]).motor
        self.motor_B = getattr(hub.port, PORT_MAP["motor_B"]).motor
        self.motor_C = getattr(hub.port, PORT_MAP["motor_C"]).motor
        self.color_sensor = getattr(hub.port, PORT_MAP["color_sensor"]).device
        self.ultrasonic_sensor = getattr(hub.port, PORT_MAP["ultrasonic_sensor"]).device
        self.serial_port = getattr(hub.port, PORT_MAP['serial_port'])
        # The port will operates as a raw full duplex logic level serial port
        self.serial_port.mode(hub.port.MODE_FULL_DUPLEX)
        # Transferring a maximum of 115200 bits per second.
        self.serial_port.baud(115200)

        image = hub.Image("99999:90090:99090:90090:99090")
        hub.display.show(image)

    def read_command(self):
        command_byte = self.serial_port.read(1)
        return int.from_bytes(command_byte, "big") if command_byte is not None else None

    def execute_command(self, command):
        if command == 1:
            self.motor_A.pwm(MOTER_POWER)
        elif command == 2:
            self.motor_B.pwm(MOTER_POWER)
        elif command == 3:
            self.motor_C.pwm(MOTER_POWER)


    def send_status(self):
        pass

    def stop_spike(self):
        self.motor_A.pwm(0)
        self.motor_B.pwm(0)
        self.motor_C.pwm(0)


async def receiver():

    while True:
        await uasyncio.sleep_ms(0)
        
        command = spike_car.read_command()
        spike_car.execute_command(command)


async def main_task():
    uasyncio.create_task(receiver())
    await uasyncio.sleep(1*60)     # Maxmium execution peroid, unit: seconds

# triggers a garbage collection cycle
gc.collect()
spike_car = SpikeCar()
uasyncio.run(main_task())