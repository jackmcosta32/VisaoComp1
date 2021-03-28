import numpy as np

from models.Actor import Actor
from models.Axis import Axis
from models.Camera import Camera
from math import pi, cos, sin


class MainController:
    def __init__(self, actor: Actor, camera: Camera):
        self.actor = actor
        self.camera = camera
        self.world_axis = Axis()

    def move_camera(
            self,
            target_point: np.ndarray = None,
            rotation_angle: float = None,
            rotation_axis: str = None
    ):
        if target_point is None:
            target_point = np.zeros(3)

        reverse_movement_matrix = self.get_reverse_movement_matrix(
            movement_matrix=self.camera.previous_movement_matrix
        )
        self.camera.move(reverse_movement_matrix)
        movement_matrix = self.get_movement_matrix(
            current_point=self.camera.coordinate,
            target_point=target_point,
            rotation_angle=rotation_angle,
            rotation_axis=rotation_axis
        )
        self.camera.move(movement_matrix)

    def move_actor(
            self,
            target_point: np.ndarray = None,
            rotation_angle: float = None,
            rotation_axis: str = None
    ):
        if target_point is None:
            target_point = np.zeros(3)

        # Reverts the previous movement
        reverse_movement_matrix = self.get_reverse_movement_matrix(
            movement_matrix=self.actor.previous_movement_matrix
        )
        self.actor.move(reverse_movement_matrix)

        # Makes the new movement
        movement_matrix = self.get_movement_matrix(
            current_point=self.actor.coordinate,
            target_point=target_point,
            rotation_angle=rotation_angle,
            rotation_axis=rotation_axis
        )
        self.actor.move(movement_matrix)

    def draw_camera_view(self):
        print('GET CAMERA VIEW')

    def draw_world_components(self, plot_axis):
        plot_axis.clear()
        self.world_axis.draw(plot_axis)
        self.actor.draw(plot_axis)
        self.camera.draw(plot_axis)

    def get_movement_matrix(
            self,
            current_point: np.ndarray,
            target_point: np.ndarray,
            rotation_angle: float = 0,
            rotation_axis: str = None,
    ):
        # Generates the new movement matrix according to the params given
        if rotation_angle is not None:
            rotation_angle = self.__degrees_to_radians(rotation_angle)

        movement_matrix = np.eye(4)
        movement_matrix[0:3, 3] = target_point - current_point

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

    def get_reverse_movement_matrix(
            self,
            movement_matrix: np.ndarray
    ):
        # Generates the reverse of a movement matrix
        reverse_movement_matrix = np.eye(4)
        previous_rotation_matrix = movement_matrix[0:3, 0:3]
        previous_translation_vector = movement_matrix[0:3, 3]

        # Reverts the previous movement
        reverse_movement_matrix[0:3, 0:3] = previous_rotation_matrix.T
        reverse_movement_matrix[0:3, 3] = - np.dot(previous_rotation_matrix.T, previous_translation_vector)

        return reverse_movement_matrix

    def __degrees_to_radians(self, degrees: float):
        return pi * degrees / 180
