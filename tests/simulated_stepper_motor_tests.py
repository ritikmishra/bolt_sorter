import math
import unittest
import time

from stepper_motor import SimulatedStepperMotor
from stepper_motor.stepper_motor_wrapper import StepperMotorWrapper
from units import Radians


class StepperMotorTests(unittest.TestCase):

    def test_sim_instantation(self):
        motor = SimulatedStepperMotor()

    def test_sim_step(self):
        motor = SimulatedStepperMotor()

        self.assertEqual(motor.get_pos(), 0)

        motor.step()

        self.assertEqual(motor.get_pos(), 1)

        motor.step(False)

        self.assertEqual(motor.get_pos(), 0)

    def test_run_to_pos(self):
        motor = SimulatedStepperMotor()

        self.assertEqual(motor.get_pos(), 0)

        def run_to_pos_and_assert(steps, rpm):
            previous_position = motor.get_pos()
            delta = steps - previous_position

            expected_revs = delta / motor.steps_per_rev
            expected_time = (expected_revs / rpm) * 60
            start = time.time()
            motor.run_to_pos(steps, rpm)
            end = time.time()

            self.assertEqual(motor.get_pos(), steps)
            self.assertAlmostEqual(abs(expected_time), end - start, delta=.05)  # allow 5% error

        run_to_pos_and_assert(200, 60)
        run_to_pos_and_assert(-50, 100)
        run_to_pos_and_assert(-150, 500)
        run_to_pos_and_assert(0, 500)

        self.assertEqual(motor.get_pos(), 0)

    def test_run_to_pos_wrapper(self):
        motor = SimulatedStepperMotor()
        gear_red = 1
        wrapper = StepperMotorWrapper(motor, gear_red)
        self.assertEqual(wrapper.get_pos(), 0)

        def run_to_pos_and_assert(rads, rpm):
            previous_position = wrapper.get_pos()
            delta: Radians = rads - previous_position

            expected_revs = delta / math.tau
            expected_time = (expected_revs / rpm) * 60
            start = time.time()
            wrapper.run_to_angle(rads, rpm)
            end = time.time()

            self.assertAlmostEqual(rads, wrapper.get_pos(), delta=.05)
            self.assertAlmostEqual(abs(expected_time), end - start, delta=1)

        run_to_pos_and_assert(200, 600)
        run_to_pos_and_assert(-50, 1000)
        run_to_pos_and_assert(-150, 500)
        run_to_pos_and_assert(0, 500)

        self.assertEqual(motor.get_pos(), 0)


if __name__ == '__main__':
    unittest.main()
