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
        self.controller.draw_world_components(plot_axis=self.world_chart.axis)
        self.world_chart.axis_equal_3D()

        return tab

    def cameraViewTab(self):
        # Setup the camera view
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_chart)
        tab.setLayout(layout)

        # Draws the camera view projection
        self.controller.draw_camera_view()

        return tab

    def actorControlsTab(self):
        # Adds the radio buttons for the reference axis selection
        ref_radio_group = QButtonGroup()
        ref_radio_layout = QHBoxLayout()
        ref_axes = ['actor', 'camera', 'world']
        for index, axis in enumerate(ref_axes):
            radio_label = '{} axis'.format(axis)
            radio = QRadioButton(radio_label)
            radio.value = axis
            ref_radio_layout.addWidget(radio)
            ref_radio_group.addButton(radio, index)

        # Sets the world axis as the default rotation axis
        ref_radio_group.button(2).setChecked(True)

        # Saves the reference for the ref radio group
        self.actor_controls['ref_radio_group'] = ref_radio_group

        # Adds the sliders layout
        sliders_layout = QGridLayout()
        sliders_layout.setSpacing(10)

        # Adds the axes sliders
        axes = ['x', 'y', 'z']
        for index, axis in enumerate(axes):
            sliders_layout.addWidget(QLabel(axis), index, 0)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-100, 100)
            slider.setValue(0)
            widget_key = '{axis}_slider'.format(axis=axis)
            self.actor_controls[widget_key] = slider
            slider.valueChanged[int].connect(self.onActorControlsChange)
            sliders_layout.addWidget(slider, index, 1)

        # Adds the radio buttons for the rotation axis selection
        rot_radio_group = QButtonGroup()
        rot_radio_layout = QHBoxLayout()
        rot_axes = ['x', 'y', 'z']
        for index, axis in enumerate(rot_axes):
            radio_label = '{} axis'.format(axis)
            radio = QRadioButton(radio_label)
            radio.value = axis
            rot_radio_layout.addWidget(radio)
            rot_radio_group.addButton(radio, index)

        # Sets the world axis as the default rotation axis
        rot_radio_group.button(2).setChecked(True)

        # Saves the reference for the rotation radio group
        self.actor_controls['rot_radio_group'] = rot_radio_group

        # Adds a dial for the actor rotation control
        dial_layout = QHBoxLayout()
        dial = QDial()
        dial.setRange(0, 360)
        self.actor_controls['rotation_dial'] = dial
        dial.valueChanged[int].connect(self.onActorControlsChange)
        dial_layout.addWidget(dial, alignment=Qt.AlignCenter)

        # Setup the tab layout
        layout = QVBoxLayout()
        layout.addLayout(ref_radio_layout)
        layout.addLayout(sliders_layout)
        layout.addLayout(rot_radio_layout)
        layout.addLayout(dial_layout)
        layout.addStretch()
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def cameraControlsTab(self):
        # Adds the radio buttons for the reference axis selection
        ref_radio_group = QButtonGroup()
        ref_radio_layout = QHBoxLayout()
        ref_axes = ['actor', 'camera', 'world']
        for index, axis in enumerate(ref_axes):
            radio_label = '{} axis'.format(axis)
            radio = QRadioButton(radio_label)
            radio.value = axis
            ref_radio_layout.addWidget(radio)
            ref_radio_group.addButton(radio, index)

        # Sets the world axis as the default rotation axis
        ref_radio_group.button(2).setChecked(True)

        # Saves the reference for the ref radio group
        self.camera_controls['ref_radio_group'] = ref_radio_group

        # Adds the sliders layout
        sliders_layout = QGridLayout()
        sliders_layout.setSpacing(10)

        # Adds the axes sliders
        axes = ['x', 'y', 'z']
        for index, axis in enumerate(axes):
            sliders_layout.addWidget(QLabel(axis), index, 0)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(-100, 100)
            slider.setValue(0)
            widget_key = '{axis}_slider'.format(axis=axis)
            self.camera_controls[widget_key] = slider
            slider.valueChanged[int].connect(self.onCameraControlsChange)
            sliders_layout.addWidget(slider, index, 1)

        # Adds the radio buttons for the rotation axis selection
        rot_radio_group = QButtonGroup()
        rot_radio_layout = QHBoxLayout()
        rot_axes = ['x', 'y', 'z']
        for index, axis in enumerate(rot_axes):
            radio_label = '{} axis'.format(axis)
            radio = QRadioButton(radio_label)
            radio.value = axis
            rot_radio_layout.addWidget(radio)
            rot_radio_group.addButton(radio, index)

        # Sets the world axis as the default rotation axis
        rot_radio_group.button(2).setChecked(True)

        # Saves the reference for the rotation radio group
        self.camera_controls['rot_radio_group'] = rot_radio_group

        # Adds a dial for the actor rotation control
        dial_layout = QHBoxLayout()
        dial = QDial()
        dial.setRange(0, 360)
        self.camera_controls['rotation_dial'] = dial
        dial.valueChanged[int].connect(self.onCameraControlsChange)
        dial_layout.addWidget(dial, alignment=Qt.AlignCenter)

        # Setup the tab layout
        layout = QVBoxLayout()
        layout.addLayout(ref_radio_layout)
        layout.addLayout(sliders_layout)
        layout.addLayout(rot_radio_layout)
        layout.addLayout(dial_layout)
        layout.addStretch()
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def onActorControlsChange(self):
        target_coordinate = np.array([
            self.actor_controls['x_slider'].value(),
            self.actor_controls['y_slider'].value(),
            self.actor_controls['z_slider'].value()
        ])

        reference_axis = self.actor_controls['ref_radio_group'].checkedButton().value
        rotation_axis = self.actor_controls['rot_radio_group'].checkedButton().value
        rotation_angle = self.actor_controls['rotation_dial'].value()

        self.controller.move_actor(
            target_coordinate=target_coordinate,
            rotation_angle=rotation_angle,
            rotation_axis=rotation_axis,
            reference_axis=reference_axis
        )
        self.controller.draw_world_components(plot_axis=self.world_chart.axis)
        self.world_chart.axis_equal_3D()

    def onCameraControlsChange(self):
        target_coordinate = np.array([
            self.camera_controls['x_slider'].value(),
            self.camera_controls['y_slider'].value(),
            self.camera_controls['z_slider'].value()
        ])

        reference_axis = self.camera_controls['ref_radio_group'].checkedButton().value
        rotation_axis = self.camera_controls['rot_radio_group'].checkedButton().value
        rotation_angle = self.camera_controls['rotation_dial'].value()

        self.controller.move_camera(
            target_coordinate=target_coordinate,
            rotation_angle=rotation_angle,
            rotation_axis=rotation_axis,
            reference_axis=reference_axis
        )
        self.controller.draw_world_components(plot_axis=self.world_chart.axis)
        self.world_chart.axis_equal_3D()

