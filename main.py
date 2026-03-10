import sys
import os
import importlib
import traceback

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QGroupBox,
    QHBoxLayout
)

from PyQt6.QtGui import QFont, QShortcut, QKeySequence
from PyQt6.QtCore import QTimer

from speech import speak, get_voices
from config.settings import settings


def safe_run(func, message=None):
    try:
        func()
        if message:
            speak(message, settings["voice"])
    except Exception:
        traceback.print_exc()
        speak("Experiment function not implemented or failed", settings["voice"])


def load_experiments():

    base_path = "experiments"
    categories = {}

    for root, dirs, files in os.walk(base_path):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                rel_path = os.path.relpath(path, base_path)
                module_path = rel_path.replace(os.sep, ".").replace(".py", "")
                module_path = "experiments." + module_path

                module = importlib.import_module(module_path)

                exp = module.Experiment()

                cat = exp.category

                if cat not in categories:
                    categories[cat] = []

                categories[cat].append(exp)

    return categories


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Accessible Experiment Platform")
        self.resize(520, 420)

        layout = QVBoxLayout()

        title = QLabel("Accessible Experiment Platform")
        layout.addWidget(title)

        accessibility_box = QGroupBox("Accessibility Settings")
        accessibility_layout = QVBoxLayout()

        font_row = QHBoxLayout()

        font_label = QLabel("Font Size")
        font_row.addWidget(font_label)

        self.font_selector = QComboBox()
        self.font_selector.addItems(
            ["Small", "Medium", "Large", "Extra Large"]
        )

        self.font_selector.currentTextChanged.connect(self.change_font)

        font_row.addWidget(self.font_selector)
        accessibility_layout.addLayout(font_row)

        voice_row = QHBoxLayout()

        voice_label = QLabel("Voice")
        voice_row.addWidget(voice_label)

        self.voice_selector = QComboBox()

        self.voices = get_voices()
        self.voice_selector.addItems(self.voices)

        self.voice_selector.currentIndexChanged.connect(self.change_voice)

        voice_row.addWidget(self.voice_selector)

        accessibility_layout.addLayout(voice_row)

        accessibility_box.setLayout(accessibility_layout)
        layout.addWidget(accessibility_box)

        experiment_box = QGroupBox("Experiments")
        experiment_layout = QVBoxLayout()

        self.categories = load_experiments()

        self.category_selector = QComboBox()
        self.category_selector.addItems(self.categories.keys())
        self.category_selector.currentIndexChanged.connect(
            self.category_changed
        )

        experiment_layout.addWidget(self.category_selector)

        self.exp_selector = QComboBox()
        self.exp_selector.currentIndexChanged.connect(
            self.experiment_changed
        )

        experiment_layout.addWidget(self.exp_selector)

        self.update_experiments()

        self.run_button = QPushButton("Open Experiment")
        self.run_button.clicked.connect(self.run_experiment)

        experiment_layout.addWidget(self.run_button)

        experiment_box.setLayout(experiment_layout)
        layout.addWidget(experiment_box)

        self.setLayout(layout)

        QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(
            self.run_experiment
        )

        self.apply_font()

        speak("Accessible Experiment Platform", settings["voice"])

        self.setTabOrder(self.font_selector, self.voice_selector)
        self.setTabOrder(self.voice_selector, self.category_selector)
        self.setTabOrder(self.category_selector, self.exp_selector)
        self.setTabOrder(self.exp_selector, self.run_button)

        self.font_selector.setFocus()

    def apply_font(self):

        font = QFont()
        font.setPointSize(settings["font_size"])
        self.setFont(font)

    def change_font(self, size):

        sizes = {
            "Small": 10,
            "Medium": 14,
            "Large": 18,
            "Extra Large": 24
        }

        settings["font_size"] = sizes[size]

        self.apply_font()

        speak(f"Font size set to {size}", settings["voice"])

    def change_voice(self, index):

        if index < len(self.voices):
            settings["voice"] = self.voices[index]

        speak(f"Voice set to {settings['voice']}", settings["voice"])

    def category_changed(self):

        category = self.category_selector.currentText()

        self.update_experiments()

        speak(f"{category} category selected", settings["voice"])

    def experiment_changed(self):

        name = self.exp_selector.currentText()

        if name:
            speak(f"{name} selected", settings["voice"])

    def update_experiments(self):

        category = self.category_selector.currentText()

        self.exp_selector.blockSignals(True)
        self.exp_selector.clear()

        for exp in self.categories[category]:
            self.exp_selector.addItem(exp.name)

        self.exp_selector.blockSignals(False)

    def run_experiment(self):

        category = self.category_selector.currentText()
        index = self.exp_selector.currentIndex()

        experiment = self.categories[category][index]

        speak(f"Opening {experiment.name}", settings["voice"])

        self.exp_window = ExperimentWindow(experiment)
        self.exp_window.show()


class ExperimentWindow(QWidget):

    def __init__(self, experiment):

        super().__init__()

        self.experiment = experiment
        self.reading_enabled = True

        self.setWindowTitle(experiment.name)
        self.resize(520, 420)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(experiment.name))
        layout.addWidget(QLabel("Aim: " + experiment.aim))
        layout.addWidget(
            QLabel("Apparatus: " + ", ".join(experiment.apparatus))
        )
        layout.addWidget(
            QLabel("Procedure: " + ", ".join(experiment.procedure))
        )

        self.toggle_button = QPushButton("Toggle Screen Reading")
        self.toggle_button.clicked.connect(self.toggle_reading)

        layout.addWidget(self.toggle_button)

        self.acquire_button = QPushButton("Acquire Data")
        self.acquire_button.clicked.connect(
            lambda: safe_run(
                self.experiment.acquire_data,
                "Data acquired"
            )
        )

        layout.addWidget(self.acquire_button)

        self.analyse_button = QPushButton("Analyse Data")
        self.analyse_button.clicked.connect(
            lambda: safe_run(
                self.experiment.analyse,
                "Analysis complete"
            )
        )

        layout.addWidget(self.analyse_button)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(
            lambda: safe_run(
                self.experiment.plot,
                "Graph generated"
            )
        )

        layout.addWidget(self.plot_button)

        self.setLayout(layout)

        self.apply_font()

        if self.reading_enabled:
            self.read_experiment()

    def apply_font(self):

        font = QFont()
        font.setPointSize(settings["font_size"])
        self.setFont(font)

    def toggle_reading(self):

        self.reading_enabled = not self.reading_enabled

        if self.reading_enabled:
            speak("Screen reading enabled", settings["voice"])
        else:
            speak("Screen reading disabled", settings["voice"])

    def read_experiment(self):

        if not self.reading_enabled:
            return

        speak(self.experiment.name, settings["voice"])

        QTimer.singleShot(
            3500,
            lambda: speak(
                f"Aim. {self.experiment.aim}. "
                f"Apparatus. {', '.join(self.experiment.apparatus)}. "
                f"Procedure. {', '.join(self.experiment.procedure)}.",
                settings["voice"]
            )
        )


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())