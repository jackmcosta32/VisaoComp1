from math import pi, cos, sin

import numpy as np

from models.Axis import Axis


class Object:
    def __init__(
            self,
            coordinate: np.ndarray = None,
    ):
        if coordinate is None:
            coordinate = np.zeros(3)

        self.coordinate = coordinate
        self.axis = Axis(coordinate=coordinate)

    def draw(self, plot_axis):
        # Draws the object axis
        self.axis.draw(plot_axis)

    def move(
            self,
            movement_matrix: np.ndarray
    ):
        # Updates the current object position according to the movement matrix
        coordinate = np.ones(4)
        coordinate[0:3] = self.coordinate
        coordinate = np.dot(movement_matrix, coordinate.T)
        self.coordinate = coordinate[0: 3]
        self.axis.coordinate = coordinate[0: 3]

    def get_movement_matrix(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None,
            target_point: np.ndarray = None,
    ):
        # Generates the movement matrix according to the params given
        if rotation_angle is not None:
            rotation_angle = self.__degrees_to_radians(rotation_angle)
        if target_point is None:
            target_point = self.coordinate

        movement_matrix = np.eye(4)
        movement_matrix[0:3, 3] = target_point - self.coordinate

        if rotation_axis == 'x':
            movement_matrix[0:3, 0:3] = np.array([
                [1, 0, 0],
                [0, cos(rotation_angle), -sin(rotation_angle)],
                [0, sin(rotation_angle), cos(rotation_angle)]
            ])
        elif rotation_axis == 'y':
            movement_matrix[0:3, 0:3] = np.array([
                [cos(rotation_angle), 0, -sin(rotation_angle)],
                [0, 1, 0],
                [sin(rotation_angle), 0, cos(rotation_angle)]
            ])
        else:
            movement_matrix[0:3, 0:3] = np.array([
                [cos(rotation_angle), -sin(rotation_angle), 0],
                [sin(rotation_angle), cos(rotation_angle), 0],
                [0, 0, 1]
            ])

        return movement_matrix

    def __degrees_to_radians(self, degrees):
        return pi * degrees / 180
