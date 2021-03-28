import cv2
import numpy as np
import matplotlib.pyplot as plt

from models.Axis import Axis
from models.Actor import Actor
from views.main.MainView import MainView


def run():
    # Intialize the view
    main_view = MainView()

    # Creating the 3D scenery
    fig = plt.figure(figsize=(15, 8))
    axis = fig.add_subplot(111, projection='3d')
    plt.ion()
    plt.title("World Point of View")

    # Creating the actors
    world_axis = Axis(plot_axis=axis)
    actor = Actor(
        plot_axis=axis,
        mesh_path="/home/joao/Documentos/Python/visao_comp1/public/stl/link.STL"
    )

    actor.move(target_point=np.array([50, 0, 0]), rotation_angle=270)
    # actor.move(target_point=np.array([50, 0, 0]), rotation_angle=45)
    # actor.move(target_point=np.array([50, 0, 0]), rotation_angle=90)
    # actor.move(target_point=np.array([50, 0, 0]), rotation_angle=270)

    while True:
        plt.show()
        plt.pause(0.5)
        fig.canvas.draw()
        fig.canvas.flush_events()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Runs the main loop
run()
