from abc import ABC, abstractmethod


# Things that you can control on an a4988l chip
# enable/disable
# microstepping: 1, 1/2, 1/4, 1/8, 1/16
# sleep
# reset
# direction
# step!

class StepperMotor(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def step(self, forwards: bool = True):
        """
        Rotate the stepper motor by 1 step. Direction indicated by `forwards`.

        :param forwards: if we should rotate forwards or backwards
        :return: None
        """
        pass

    @abstractmethod
    def get_pos(self):
        """
        Returns the actual number of steps this motor has traveled.

        :return: position of motor shaft
        """
        pass

    @abstractmethod
    def run_to_pos(self, desired_pos, rpm):
        """
        Run the motor shaft until we reach a desired position. This is a blocking method.

        :param desired_pos: The desired end position. The "step" nature of a stepper motor may make it impossible to
        reach it exactly, but we will get as close as we can.

        :param rpm: How fast to go to the end position (rotations/minute).

        :return: The actual end position.
        """

    @abstractmethod
    def set_enabled(self, is_enabled: bool):
        """
        Enable/disable the motor. Useful for low-power control modes.

        :param is_enabled:
        :return: None
        """
        pass
