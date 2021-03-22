import numpy as np


class Axis:
    def __init__(
            self,
            plot_axis,
            length: float = 1,
            base: np.ndarray = None,
            coordinate: np.ndarray = None
    ):

        if base is None:
            base = np.eye(3)
        if coordinate is None:
            coordinate = np.zeros(3)

        self.base = base
        self.length = length
        self.plot_axis = plot_axis
        self.coordinate = coordinate
        previous_movement_matrix = np.eye(4)
        previous_movement_matrix[0:3, 3] = coordinate
        self.previous_movement_matrix = previous_movement_matrix

    def draw(self):
        self.plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[0][0],
            self.base[0][1],
            self.base[0][2],
            color='red',
            pivot='tail',
            length=self.length
        )

        self.plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[1][0],
            self.base[1][1],
            self.base[1][2],
            color='green',
            pivot='tail',
            length=self.length
        )

        self.plot_axis.quiver(
            self.coordinate[0],
            self.coordinate[1],
            self.coordinate[2],
            self.base[2][0],
            self.base[2][1],
            self.base[2][2],
            color='blue',
            pivot='tail',
            length=self.length
        )
