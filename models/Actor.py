import numpy as np
from mpl_toolkits.mplot3d import art3d
from stl import mesh

from models.Object import Object


class Actor(Object):
    def __init__(
            self,
            mesh_path: str,
            coordinate: np.ndarray = None,
    ):
        # Obtains the actor mesh vectors and points
        object_mesh = mesh.Mesh.from_file(mesh_path)
        x = object_mesh.x.flatten()
        y = object_mesh.y.flatten()
        z = object_mesh.z.flatten()
        self.mesh_vectors = object_mesh.vectors
        self.mesh_matrix = np.array([x.T, y.T, z.T, np.ones(x.size)])

        # Init object
        super().__init__(coordinate=coordinate)

    def draw(self, plot_axis):
        # Draws the actor mesh surfaces and lines
        plot_axis.plot(self.mesh_matrix[0, :], self.mesh_matrix[1, :], self.mesh_matrix[2, :], 'b')
        # plot_axis.add_collection3d(art3d.Poly3DCollection(self.mesh_vectors))
        # plot_axis.add_collection3d(art3d.Line3DCollection(
        #     self.mesh_vectors,
        #     colors='k',
        #     linewidths=0.2,
        #     linestyles='-'
        # ))

        # Draws the object axis
        super().draw(plot_axis)

    def move(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None,
            target_point: np.ndarray = None,
    ):
        # Extends the object movement to include the mesh movement
        movement_matrix = super().get_movement_matrix(
            target_point=target_point,
            rotation_axis=rotation_axis,
            rotation_angle=rotation_angle,
        )

        # Updates the actor mesh matrix
        new_mesh_matrix = np.ones(self.mesh_matrix.shape)
        for i in range(self.mesh_matrix.shape[1]):
            coordinate = self.mesh_matrix[:, i]
            coordinate = np.dot(movement_matrix, coordinate.T)
            new_mesh_matrix[:, i] = coordinate

        self.mesh_matrix = new_mesh_matrix

        # Updates the actor axis coordinates
        super().move(movement_matrix=movement_matrix)