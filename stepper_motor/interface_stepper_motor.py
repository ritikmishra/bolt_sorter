from abc import ABC, abstractmethod


# Things that you can control on an a4988l chip
# enable/disable
# microstepping: 1, 1/2, 1/4, 1/8, 1/16
# sleep
# reset
# direction
# step!
DEFAULT_STEPS_PER_REV = 200

class StepperMotor(ABC):
    def __init__(self, steps_per_rev=DEFAULT_STEPS_PER_REV):
        super().__init__()
        self.steps_per_rev = steps_per_rev


    @abstractmethod
    def step(self, forwards: bool = True):
        """
        Rotate the stepper motor by 1 step. Direction indicated by `forwards`.
        Near instant.

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
    def get_revs(self):
        """
        Returns the number of revolutions this motor has completed

        :return:
        """
        pass

    @abstractmethod
    def reset_pos(self, new_pos_val=0):
        """
        Reset the measured pose based on other sensor input e.g a limit switch

        :param new_pos_val: The new recorded current position. Default: 0
        :return: None
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
