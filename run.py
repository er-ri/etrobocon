import time
from etrobocon import ETRobot

et = ETRobot()

while et.terminated == False:
    # Get camera capture
    # Set section data
    # Get operation command(manually or by Nvidia Model)
    time.sleep(0.05)  # 20 fps


del et
