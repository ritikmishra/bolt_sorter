#!/usr/bin/python3
import threading
import time
import tkinter
import numpy as np
import random
from stepper_motor import SimulatedStepperMotor
from stepper_motor.stepper_motor_wrapper import StepperMotorWrapper
from superstructure import SuperstructureController
from units import Inches

top = tkinter.Tk()

h = 900
w = 900


def convert_from_math_to_tk(coords):
    coords[1] *= -1
    coords += np.array([w / 2.0, h / 2.0], dtype=np.int64)
    return coords


c = tkinter.Canvas(top, height=h, width=w)

turret_motor = StepperMotorWrapper(SimulatedStepperMotor(), 1 / 12)
joint_1_motor = StepperMotorWrapper(SimulatedStepperMotor(), 1 / 5)
joint_2_motor = StepperMotorWrapper(SimulatedStepperMotor(), 1 / 5)

superstructure = SuperstructureController(turret_motor, joint_1_motor, joint_2_motor, Inches(5), Inches(5))

# superstructure.go_to_point(np.array([[3], [0], [3]], dtype=np.int64))
goal_x = 2
goal_y = 4
new_goal = True


def move_arm_around():
    global goal_x, goal_y, superstructure, new_goal
    while True:
        goal_x = random.uniform(0, 5)
        goal_y = random.uniform(-5, 5)
        new_goal = True

        try:
            superstructure.go_to_point(np.array([[goal_x], [0], [goal_y]]), idx=random.randint(0, 1))
        except ValueError:
            pass


# thread = threading.Thread(target=superstructure.go_to_point, args=(np.array([[goal_x], [0], [goal_y]], dtype=np.int64),))
thread = threading.Thread(target=move_arm_around)
thread.start()

px_over_in = 50

if __name__ == '__main__':
    # Code to add widgets will go here...
    while True:
        print(joint_1_motor.get_pos(), joint_2_motor.get_pos())
        c.delete("all")

        origin = np.array([0, 0])

        joint_1_end_loc = superstructure.kh.get_joint_1_length() * px_over_in * \
                          np.array([np.cos(joint_1_motor.get_pos()),
                                    np.sin(joint_1_motor.get_pos())])

        joint_2_end_loc = superstructure.kh.get_joint_2_length() * px_over_in * \
                          np.array([np.cos(joint_2_motor.get_pos() + joint_1_motor.get_pos()),
                                    np.sin(joint_2_motor.get_pos() + joint_1_motor.get_pos())])

        joint_2_end_loc += joint_1_end_loc

        origin = convert_from_math_to_tk(origin)
        joint_1_end_loc = convert_from_math_to_tk(joint_1_end_loc)
        joint_2_end_loc = convert_from_math_to_tk(joint_2_end_loc)

        joint_1_line = c.create_line(*origin, *joint_1_end_loc)
        joint_2_line = c.create_line(*joint_1_end_loc, *joint_2_end_loc, fill="red")

        if new_goal:
            goal_x *= px_over_in
            goal_y *= px_over_in

            goal_x, goal_y = convert_from_math_to_tk(np.array([goal_x, goal_y]))
            new_goal = False

        goal_pt = c.create_oval(goal_x - 5, goal_y - 5, goal_x + 5, goal_y + 5)

        c.pack()
        top.update()
