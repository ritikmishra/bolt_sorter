import unittest
import time

from stepper_motor.simulated_stepper_motor import SimulatedStepperMotor


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


if __name__ == '__main__':
    unittest.main()
