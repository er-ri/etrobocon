"""Line follower

The module contains line follower implementation of camera based and colorsensor based, 
which are used for training data collection for the model. By sending the input data
such as camera image or sensor status, the function will return the steering angle. 
"""


def follow_line_by_camera():
    raise NotImplementedError


def follow_line_by_sensor():
    raise NotImplementedError
