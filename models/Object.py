from math import pi, cos, sin

import numpy as np

from models.Axis import Axis


class Object:
    def __init__(
            self,
            plot_axis,
            coordinate: np.ndarray = None,
    ):
        self.plot_axis = plot_axis
        self.coordinate = coordinate
        self.axis = Axis(plot_axis=plot_axis, coordinate=coordinate)

    def draw(self):
        self.axis.draw()

    def move(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None,
            target_point: np.ndarray = None,
    ):
        # Obtain current movement matrix
        movement_matrix = self.__get_movement_matrix(
            rotation_angle=rotation_angle,
            rotation_axis=rotation_axis,
            target_point=target_point
        )

        # Revert previous movement
        # previous_movement_matrix = self.previous_movement_matrix
        # previous_rotation_matrix = previous_movement_matrix[0:3, 0:3]
        # previous_movement_matrix[0:3, 0:3] = previous_rotation_matrix.T
        # previous_translation = previous_movement_matrix[0:3, 3]
        # previous_movement_matrix[0:3, 3] = -np.dot(previous_rotation_matrix.T, previous_translation)

        # Make the new transformation
        coordinate = np.ones(4)
        coordinate[0:3] = self.coordinate
        # coordinate = np.dot(np.dot(previous_movement_matrix, movement_matrix), coordinate.T)
        coordinate = np.dot(movement_matrix, coordinate.T)
        # self.previous_movement_matrix = movement_matrix
        self.coordinate = coordinate[0: 3]
        self.draw()

    def __get_movement_matrix(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None,
            target_point: np.ndarray = None,
    ):
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
