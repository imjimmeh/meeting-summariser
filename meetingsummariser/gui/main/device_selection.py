from pyaudio import PyAudio
from PyQt6.QtWidgets import QCheckBox, QLabel, QLayout, QWidget

from meetingsummariser.gui.shared.collapsable_frame import CollapsibleFrame

show_devices_text = "Select devices"
hide_devices_text = "Hide devices"


class DeviceSelection(CollapsibleFrame):
    devices = []

    def __init__(
        self, parent: QWidget, parent_layout: QLayout, pyaudio_instance: PyAudio
    ):
        super().__init__(parent, parent_layout)
        self.pyaudio_instance = pyaudio_instance
        self.create_label()
        self.create_device_selection_ui()

    def list_audio_devices(self):
        num_devices = self.pyaudio_instance.get_device_count()
        devices = []

        for i in range(num_devices):
            device_info = self.pyaudio_instance.get_device_info_by_index(i)
            max_input_channels = device_info.get("maxInputChannels")
            if max_input_channels is not None and int(max_input_channels) > 0:
                devices.append((i, device_info.get("name")))

        return devices

    def create_label(self):
        self.label = QLabel("Device selection")
        self.layout.addWidget(self.label)

    def create_device_selection_ui(self):
        devices = self.list_audio_devices()
        self.devices = devices

        self.device_vars = []
        self.device_labels = []

        for i, (index, name) in enumerate(devices):
            checkbox = QCheckBox(name)
            self.layout.addWidget(checkbox)
            self.device_vars.append(checkbox)

    def get_selected_device_indices(self):
        return [
            index
            for i, (index, name) in enumerate(self.devices)
            if self.device_vars[i].isChecked()
        ]

    def on_hiding(self):
        self.toggle_button.setText(show_devices_text)

    def on_showing(self):
        self.toggle_button.setText(hide_devices_text)
