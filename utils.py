import math

from units import Radians


def bound_angle(angle: Radians) -> Radians:
    while angle < -math.pi:
        angle += math.tau

    while angle > math.pi:
        angle -= math.tau

    return angle
