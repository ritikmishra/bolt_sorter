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
        return self._motor.get_revs() * self.output_radians_over_input_revs

    def run_to_angle(self, target_radians: Radians, target_output_rpm):
        target_pos_revs = target_radians / self.output_radians_over_input_revs
        target_pos_steps = target_pos_revs * self._motor.steps_per_rev
        target_motor_rpm = target_output_rpm * math.tau / self.output_radians_over_input_revs

        self._motor.run_to_pos(target_pos_steps, target_motor_rpm)

        return self.get_pos()

    def reset_pos(self, new_val_radians: Radians = 0):
        self._motor.reset_pos(new_val_radians / self.output_radians_over_input_revs)
