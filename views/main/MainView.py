import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.Chart import Chart
from controllers.MainController import MainController


class MainView(QMainWindow):
    def __init__(self, controller: MainController):
        super().__init__()

        # Setup view params
        self.setWindowTitle('Visão Comp. - Trabalho 1')
        self.resize(270, 110)
        self.controller = controller
        self.actor_controls = {}
        self.camera_controls = {}

        # Setup view layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # Setup the camera and world views tab
        self.camera_chart = Chart(
            title='camera view',
            # ion=True
        )
        self.world_chart = Chart(
            title='world view',
            aspect='equal',
            projection='3d',
            ion=True
        )
        visualization_tabs = QTabWidget()
        visualization_tabs.addTab(self.worldViewTab(), 'World View')
        visualization_tabs.addTab(self.cameraViewTab(), 'Camera View')

        # Setup the controls tabs
        control_tabs = QTabWidget()
        control_tabs.addTab(self.actorControlsTab(), 'Actor Controls')
        control_tabs.addTab(self.cameraControlsTab(), 'Camera Controls')

        # Add tabs to the layout
        main_layout.addWidget(visualization_tabs)
        main_layout.addWidget(control_tabs)

        # Join the page content
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def worldViewTab(self):
        # Setup the world view
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.world_chart)
        tab.setLayout(layout)

        # Draws the world actors
        self.controller.drawWorldComponents(plot_axis=self.world_chart.axis)
        self.world_chart.axisEqual3D()

        return tab

    def cameraViewTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_chart)
        tab.setLayout(layout)
        return tab

    def actorControlsTab(self):
        sliders_layout = QGridLayout()
        sliders_layout.setSpacing(10)

        # Adds the axes sliders
        axes = ['x', 'y', 'z']
        for index, axis in enumerate(axes):
            sliders_layout.addWidget(QLabel(axis), index, 0)
            slider = QSlider(Qt.Horizontal)
            widget_key = '{axis}_slider'.format(axis=axis)
            self.actor_controls[widget_key] = slider
            slider.valueChanged[int].connect(self.onActorControlsChange)
            sliders_layout.addWidget(slider, index, 1)

        # Adds a knob for the actor rotation control
        dial_layout = QHBoxLayout()
        dial = QDial()
        dial.setRange(0, 360)
        self.actor_controls['rotation_dial'] = dial
        dial.valueChanged[int].connect(self.onActorControlsChange)
        dial_layout.addWidget(dial, alignment=Qt.AlignCenter)

        # Setup the tab layout
        layout = QVBoxLayout()
        layout.addLayout(sliders_layout)
        layout.addLayout(dial_layout)
        layout.addStretch()
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def cameraControlsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Camera Option 1"))
        layout.addWidget(QCheckBox("Camera Option 2"))
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def onActorControlsChange(self):
        target_point = np.array([
            self.actor_controls['x_slider'].value(),
            self.actor_controls['y_slider'].value(),
            self.actor_controls['z_slider'].value()
        ])
        rotation_angle = self.actor_controls['rotation_dial'].value()
        self.controller.moveActor(target_point=target_point, rotation_angle=rotation_angle)
        self.controller.drawWorldComponents(plot_axis=self.world_chart.axis)
        self.world_chart.axisEqual3D()

