import math

import numpy as np
import unittest

from superstructure import KinematicsHelper
from units import Inches


class KinematicsHelperTests(unittest.TestCase):
    def setUp(self):
        self.joint_1_length = Inches(4)
        self.joint_2_length = Inches(4)
        self.total_length = self.joint_1_length + self.joint_2_length
        self.kh = KinematicsHelper(self.joint_1_length, self.joint_2_length)

    def test_forwards_kinematics(self):
        # rotating on the azimuth when straight up should not change anything
        straight_up = [np.array([[0], [math.pi / 2], [0]]),
                       np.array([[3], [math.pi / 2], [0]]),
                       np.array([[5], [math.pi / 2], [0]])]

        for pos in straight_up:
            np.testing.assert_array_almost_equal(self.kh.forwards_kinematics(pos),
                                                 np.array([[0], [0], [self.total_length]]))

        flat = np.array([[0], [0], [0]])
        np.testing.assert_array_almost_equal(
            self.kh.forwards_kinematics(flat),
            np.array([[self.total_length], [0], [0]])
        )

        flat_but_on_y_axis = np.array([[math.pi / 2], [0], [0]])
        np.testing.assert_array_almost_equal(
            self.kh.forwards_kinematics(flat_but_on_y_axis),
            np.array([[0], [self.total_length], [0]])
        )

        diagonal_xyplane = np.array([[math.pi / 4], [0], [0]])
        np.testing.assert_array_almost_equal(
            self.kh.forwards_kinematics(diagonal_xyplane),
            np.array([[self.total_length / math.sqrt(2)], [self.total_length / math.sqrt(2)], [0]])
        )

        origin = np.array([[69], [math.pi / 3], [math.pi]])
        np.testing.assert_array_almost_equal(
            self.kh.forwards_kinematics(origin),
            np.array([[0], [0], [0]])
        )

        # TODO: Add more test cases

    def test_inverse_kinematics(self):
        poses_to_try = [
            np.array([[0], [0], [0]]),
            np.array([[0], [0], [1]]),
            np.array([[0], [0], [2]]),
            np.array([[0], [0], [3]]),
            np.array([[0], [1], [0]]),
            np.array([[0], [1], [1]]),
            np.array([[0], [1], [2]]),
            np.array([[0], [1], [3]]),
            np.array([[0], [2], [0]]),
            np.array([[0], [2], [1]]),
            np.array([[0], [2], [2]]),
            np.array([[0], [2], [3]]),
            np.array([[0], [3], [0]]),
            np.array([[0], [3], [1]]),
            np.array([[0], [3], [2]]),
            np.array([[0], [3], [3]]),
            np.array([[1], [0], [0]]),
            np.array([[1], [0], [1]]),
            np.array([[1], [0], [2]]),
            np.array([[1], [0], [3]]),
            np.array([[1], [1], [0]]),
            np.array([[1], [1], [1]]),
            np.array([[1], [1], [2]]),
            np.array([[1], [1], [3]]),
            np.array([[1], [2], [0]]),
            np.array([[1], [2], [1]]),
            np.array([[1], [2], [2]]),
            np.array([[1], [2], [3]]),
            np.array([[1], [3], [0]]),
            np.array([[1], [3], [1]]),
            np.array([[1], [3], [2]]),
            np.array([[1], [3], [3]]),
            np.array([[2], [0], [0]]),
            np.array([[2], [0], [1]]),
            np.array([[2], [0], [2]]),
            np.array([[2], [0], [3]]),
            np.array([[2], [1], [0]]),
            np.array([[2], [1], [1]]),
            np.array([[2], [1], [2]]),
            np.array([[2], [1], [3]]),
            np.array([[2], [2], [0]]),
            np.array([[2], [2], [1]]),
            np.array([[2], [2], [2]]),
            np.array([[2], [2], [3]]),
            np.array([[2], [3], [0]]),
            np.array([[2], [3], [1]]),
            np.array([[2], [3], [2]]),
            np.array([[2], [3], [3]]),
            np.array([[3], [0], [0]]),
            np.array([[3], [0], [1]]),
            np.array([[3], [0], [2]]),
            np.array([[3], [0], [3]]),
            np.array([[3], [1], [0]]),
            np.array([[3], [1], [1]]),
            np.array([[3], [1], [2]]),
            np.array([[3], [1], [3]]),
            np.array([[3], [2], [0]]),
            np.array([[3], [2], [1]]),
            np.array([[3], [2], [2]]),
            np.array([[3], [2], [3]]),
            np.array([[3], [3], [0]]),
            np.array([[3], [3], [1]]),
            np.array([[3], [3], [2]]),
            np.array([[3], [3], [3]]),

        ]

        for expected_pose in poses_to_try:
            joint_angle_options = self.kh.inverse_kinematics(expected_pose)

            for joint_angles in joint_angle_options:
                actual_pose = self.kh.forwards_kinematics(joint_angles)
                np.testing.assert_array_almost_equal(expected_pose, actual_pose, err_msg="Expected pose not equal to actual pose")


if __name__ == '__main__':
    unittest.main()
