class PIDController:
    """
    A PID (Proportional-Integral-Derivative) controller is a control loop mechanism widely used in industrial control systems.
    This class implements a basic PID controller.

    Attributes:
        Kp (float): Proportional gain.
        Ki (float): Integral gain.
        Kd (float): Derivative gain.
        setpoint (float): Desired value that the system should achieve.
        output_limits (tuple[int, int]): Minimum and maximum limits for the output.
        _previous_error (float): Error from the previous update, used to calculate the derivative term.
        _integral (float): Accumulated integral of the error over time.
    """

    def __init__(
        self,
        Kp: float,
        Ki: float,
        Kd: float,
        setpoint: float,
        output_limits: tuple[float, float] = (None, None),
    ):
        """
        Initializes the PIDController with the specified gains, setpoint, and output limits.

        Args:
            Kp (float): Proportional gain.
            Ki (float): Integral gain.
            Kd (float): Derivative gain.
            setpoint (float): Desired value that the system should achieve.
            output_limits (tuple[float, float], optional): Minimum and maximum limits for the output. Defaults to (None, None).
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        self._previous_error = 0.0
        self._integral = 0.0

    def update(self, measured_value: float, delta_time: float) -> int:
        """
        Calculate the control variable based on the measured value.

        Args:
            measured_value (float): The current value of the process variable.
            delta_time (float): Interval between two updates.

        Returns:
            int: Control output, typically used for wheel steering or other control mechanisms.
        """
        error = self.setpoint - measured_value
        self._integral += error * delta_time
        derivative = (
            (error - self._previous_error) / delta_time if delta_time > 0 else 0.0
        )

        output = self.Kp * error + self.Ki * self._integral + self.Kd * derivative

        self._previous_error = error

        # Apply output limits
        if self.output_limits[0] is not None:
            output = max(self.output_limits[0], output)
        if self.output_limits[1] is not None:
            output = min(self.output_limits[1], output)

        return int(output)
