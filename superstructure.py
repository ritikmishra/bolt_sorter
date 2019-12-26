from typing import Tuple

import numpy as np

from stepper_motor import SimulatedStepperMotor
import math

from stepper_motor.stepper_motor_wrapper import StepperMotorWrapper
from units import Inches, Radians
from utils import bound_angle


class KinematicsHelper(object):
    def __init__(self, joint_1_length: Inches = 4, joint_2_length: Inches = 4):
        self._joint_1_length: Inches = joint_1_length
        self._joint_2_length: Inches = joint_2_length

    def inverse_kinematics(self, desired_end_location: np.array) -> Tuple[np.array, np.array]:
        # it will now be a 1D array
        desired_end_location = desired_end_location.flatten()

        r = np.linalg.norm(desired_end_location)
        theta = math.atan2(desired_end_location[1], desired_end_location[0])

        if r != 0:
            rho = math.acos(desired_end_location[2] / r)
        else:
            rho = 0  # if r is 0, then rho can be anything and it will still point to the origin

        turret_angle = Radians(theta)  # Mathematics convention: theta is the heading

        # we are now working in the "r-z" plane, coplanar with the angle rho
        rhos_compliment = math.pi / 2 - rho
        rz_desired_end_loc = (r * np.array([[math.cos(rhos_compliment)],
                                            [math.sin(rhos_compliment)]]))

        d = np.linalg.norm(rz_desired_end_loc)
        r0 = self._joint_1_length
        r1 = self._joint_2_length

        if d > r0 + r1 or d < abs(r0 - r1):
            # circles completely outside or inside each other, circumfrence not intersecting
            raise ValueError(
                "desired_end_location impossible given current joint lengths.\ndesired_end_location:\n{}".format(
                    desired_end_location))
        elif d == 0:
            if r0 != r1:
                raise ValueError(
                    "desired_end_location impossible given current joint lengths.\ndesired_end_location:\n{}".format(
                        desired_end_location))
            else:  # r0 == r1
                x3 = r0
                y3 = 0

                x4 = 0
                y4 = r0
        else:
            a = (r0 * r0 - r1 * r1 + d * d) / (2 * d)
            h = math.sqrt(r0 * r0 - a * a)

            midpoint_between_circles = ((a / d) * rz_desired_end_loc).flatten()

            x3 = midpoint_between_circles[0] + h * (rz_desired_end_loc[1, 0]) / d
            y3 = midpoint_between_circles[1] - h * (rz_desired_end_loc[0, 0]) / d

            x4 = midpoint_between_circles[0] - h * (rz_desired_end_loc[1, 0]) / d
            y4 = midpoint_between_circles[1] + h * (rz_desired_end_loc[0, 0]) / d

        def calc_joint_angles(corner_point: np.array) -> np.array:
            joint_1_angle = Radians(math.atan2(corner_point[1, 0], corner_point[0, 0]))

            joint_2_vec = rz_desired_end_loc - corner_point
            joint_2_angle = Radians(math.atan2(joint_2_vec[1, 0], joint_2_vec[0, 0]))
            joint_2_angle -= joint_1_angle  # absolute to relative

            return np.array([[bound_angle(turret_angle)],
                             [bound_angle(joint_1_angle)],
                             [bound_angle(joint_2_angle)]])

        return (calc_joint_angles(np.array([[x3], [y3]])),
                calc_joint_angles(np.array([[x4], [y4]])))

        # TODO: collision checking?
        # TODO: should we return something else than a np.array? a namedtuple? idk

    def forwards_kinematics(self, current_pose: np.array) -> np.array:
        current_pose = current_pose.flatten()

        current_pose[2] += current_pose[1]  # relative to absolute

        theta = current_pose[0]

        joint_1 = self._joint_1_length * np.array([[math.cos(current_pose[1])],
                                                   [math.sin(current_pose[1])]])

        joint_2 = self._joint_2_length * np.array([[math.cos(current_pose[2])],
                                                   [math.sin(current_pose[2])]])

        end_effector = joint_1 + joint_2

        r = np.linalg.norm(end_effector)
        end_effector_unit = (end_effector / r).flatten()

        # need to subtract half-pi because rho is angle down from z, not angle up from xy
        rho = math.pi / 2 - math.atan2(end_effector_unit[1], end_effector_unit[0])

        x = r * math.sin(rho) * math.cos(theta)
        y = r * math.sin(rho) * math.sin(theta)
        z = r * math.cos(rho)

        return np.array([[x],
                         [y],
                         [z]])


