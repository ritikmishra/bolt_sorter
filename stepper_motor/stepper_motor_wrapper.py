import math

from stepper_motor import StepperMotor
from units import Radians


class StepperMotorWrapper(object):
    def __init__(self, motor: StepperMotor, gear_reduction: float):
        self._motor = motor

        # There are 2pi radians per revolution
        # There are gear_reduction output revs per input rev
        self.output_radians_over_input_revs = gear_reduction * 2 * math.pi

    def get_pos(self) -> Radians:
        """
        :return: Get the angular position of the stepper motor in radians
        """
        return self._motor.get_revs() * self.output_radians_over_input_revs

    def run_to_angle(self, target_radians: Radians, target_radians_per_sec):
        """
        Drive the stepper motor to a location in the preferred units
        :param target_radians:
        :param target_radians_per_sec:
        :return:
        """
        target_pos_revs = target_radians / self.output_radians_over_input_revs
        target_vel_rpm = target_radians_per_sec * 60 / self.output_radians_over_input_revs

        return self._motor.run_to_pos(target_pos_revs, target_vel_rpm)

    def reset_pos(self, new_val_radians: Radians = 0):
        """
        Override the read value
        :param new_val_radians:
        :return:
        """
        self._motor.reset_pos(new_val_radians / self.output_radians_over_input_revs)
