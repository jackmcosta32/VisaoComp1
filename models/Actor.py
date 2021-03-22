import numpy as np
from mpl_toolkits.mplot3d import art3d
from stl import mesh

from models.Object import Object


class Actor(Object):
    def __init__(
            self,
            plot_axis,
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
        super().__init__(plot_axis=plot_axis, coordinate=coordinate)

    def draw(self):
        # Draws the actor mesh surfaces and lines
        self.plot_axis.plot(self.mesh_matrix[0, :], self.mesh_matrix[1, :], self.mesh_matrix[2, :], 'b')
        self.plot_axis.add_collection3d(art3d.Poly3DCollection(self.mesh_vectors))
        self.plot_axis.add_collection3d(art3d.Line3DCollection(
            self.mesh_vectors,
            colors='k',
            linewidths=0.2,
            linestyles='-'
        ))

        # Draws the object axis
        super().draw()

    def move(
            self,
            rotation_angle: float = 0,
            rotation_axis: str = None,
            target_point: np.ndarray = None,
    ):
        # Extends the object movement to include the mesh movement
        movement_matrix = super().__get_movement_matrix(
            target_point=target_point,
            rotation_axis=rotation_axis,
            rotation_angle=rotation_angle,
        )

        # Updates the actor mesh matrix
        new_mesh_matrix = np.zeros(self.mesh_matrix.shape)
        for i in range(self.mesh_matrix.shape[1]):
            coordinate = np.ones(4)
            coordinate[0:3] = self.mesh_matrix[0:3, i]
            coordinate = np.dot(movement_matrix, coordinate.T)
            new_mesh_matrix[0:3, i] = coordinate[0:3, i]

        # Updates the actor axis coordinates

