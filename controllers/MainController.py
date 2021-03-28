import numpy as np

from models.Actor import Actor
from models.Axis import Axis
from models.Camera import Camera


class MainController:
    def __init__(self, actor: Actor, camera: Camera):
        self.actor = actor
        self.camera = camera
        self.world_axis = Axis()

    def moveCamera(
            self,
            target_point: list = np.array([0, 0, 0]),
            rotation_angle: float = None
    ):
        print(target_point, rotation_angle)

    def getCameraView(self):
        print('GET CAMERA VIEW')

    def moveActor(
            self,
            target_point: list = np.array([0, 0, 0]),
            rotation_angle: float = None,
            rotation_axis: str = None
    ):
        self.actor.move(
            rotation_angle=rotation_angle,
            target_point=target_point
        )

    def drawWorldComponents(self, plot_axis):
        plot_axis.clear()
        self.world_axis.draw(plot_axis)
        self.actor.draw(plot_axis)
        self.camera.draw(plot_axis)
