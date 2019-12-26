from stepper_motor import StepperMotor
import time

DEFAULT_STEPS_PER_REV = 200


class SimulatedStepperMotor(StepperMotor):
    def __init__(self, steps_per_rev=DEFAULT_STEPS_PER_REV):
        super().__init__()
        self.steps_per_rev = steps_per_rev

        self._position_counter = 0
        self._overflow = 0

    def step(self, forwards: bool = True):
        if forwards:
            self._position_counter += 1
        else:
            self._position_counter -= 1

    def get_pos(self):
        return self._position_counter

    def get_revs(self):
        return self._position_counter / self.steps_per_rev

    def reset_pos(self, new_pos_val=0):
        self._position_counter = new_pos_val

    def run_to_pos(self, desired_steps, rpm):
        secs_per_step = 60 / (rpm * self.steps_per_rev)

        # TODO: Support microstepping?
        self._overflow += desired_steps % 1
        desired_steps = int(desired_steps // 1)

        if self._overflow > 1:
            desired_steps += self._overflow // 1
            self._overflow -= self._overflow // 1

        if desired_steps == self._position_counter:
            return self._position_counter

        steps_to_take = abs(desired_steps - self._position_counter)
        forwards = desired_steps > self._position_counter

        assert int(steps_to_take) == steps_to_take
        for _ in range(int(steps_to_take)):
            self.step(forwards)
            time.sleep(secs_per_step)

        return self._position_counter

    def set_enabled(self, is_enabled: bool):
        """
        Does nothing for a simulated motor
        :param is_enabled:
        :return:
        """
        pass
