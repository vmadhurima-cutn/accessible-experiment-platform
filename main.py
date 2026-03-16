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

from PyQt6.QtGui import (
    QFont,
    QShortcut,
    QKeySequence,
    QFontDatabase,
    QDesktopServices
)

from PyQt6.QtCore import QTimer, QUrl

from speech import speak, get_voices
from config.settings import settings


loaded_fonts = []
font_lookup = {}


def load_fonts():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(script_dir, "fonts")

    if not os.path.exists(font_dir):
        return

    for file in os.listdir(font_dir):

        if file.lower().endswith(".ttf") or file.lower().endswith(".otf"):

            path = os.path.join(font_dir, file)

            font_id = QFontDatabase.addApplicationFont(path)

            if font_id == -1:
                continue

            families = QFontDatabase.applicationFontFamilies(font_id)

            for fam in families:

                styles = QFontDatabase.styles(fam)

                for style in styles:

                    label = f"{fam} {style}"

                    if label not in font_lookup:
                        loaded_fonts.append(label)
                        font_lookup[label] = (fam, style)

    loaded_fonts.sort()


def apply_global_font():

    if settings["font_family"] == "Default":

        font = QFont()
        font.setPointSize(settings["font_size"])

    else:

        font = QFontDatabase.font(
            settings["font_family"],
            settings["font_style"],
            settings["font_size"]
        )

    QApplication.instance().setFont(font)


def safe_run(func):

    try:
        func()

    except Exception:

        traceback.print_exc()


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

        self.font_selector.currentTextChanged.connect(
            self.change_font_size
        )

        font_row.addWidget(self.font_selector)
        accessibility_layout.addLayout(font_row)

        font_family_row = QHBoxLayout()

        font_family_label = QLabel("Font Type")
        font_family_row.addWidget(font_family_label)

        self.font_family_selector = QComboBox()
        self.font_family_selector.addItem("Default")

        for f in loaded_fonts:
            self.font_family_selector.addItem(f)

        self.font_family_selector.currentTextChanged.connect(
            self.change_font_family
        )

        font_family_row.addWidget(self.font_family_selector)
        accessibility_layout.addLayout(font_family_row)

        voice_row = QHBoxLayout()

        voice_label = QLabel("Voice")
        voice_row.addWidget(voice_label)

        self.voice_selector = QComboBox()

        self.voices = sorted(set(get_voices()))
        self.voice_selector.addItems(self.voices)

        self.voice_selector.currentIndexChanged.connect(
            self.change_voice
        )

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

        QShortcut(
            QKeySequence("Ctrl+O"),
            self
        ).activated.connect(self.run_experiment)

        apply_global_font()

        speak("Accessible Experiment Platform", settings["voice"])

        self.font_selector.setFocus()

    def change_font_size(self, size):

        sizes = {
            "Small": 10,
            "Medium": 14,
            "Large": 18,
            "Extra Large": 24
        }

        settings["font_size"] = sizes[size]

        apply_global_font()

        speak(
            f"Font size set to {size}",
            settings["voice"]
        )

    def change_font_family(self, label):

        if label == "Default":

            settings["font_family"] = "Default"
            settings["font_style"] = ""

        else:

            family, style = font_lookup[label]

            settings["font_family"] = family
            settings["font_style"] = style

        apply_global_font()

        speak(
            f"Font style set to {label}",
            settings["voice"]
        )

    def change_voice(self, index):

        if index < len(self.voices):
            settings["voice"] = self.voices[index]

        speak(
            f"Voice set to {settings['voice']}",
            settings["voice"]
        )

    def category_changed(self):

        category = self.category_selector.currentText()

        self.update_experiments()

        speak(
            f"{category} category selected",
            settings["voice"]
        )

    def experiment_changed(self):

        name = self.exp_selector.currentText()

        if name:
            speak(
                f"{name} selected",
                settings["voice"]
            )

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

        speak(
            f"Opening {experiment.name}",
            settings["voice"]
        )

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

        self.instructions_button = QPushButton("Full Instructions")
        self.instructions_button.clicked.connect(self.open_instructions)
        layout.addWidget(self.instructions_button)

        self.toggle_button = QPushButton("Toggle Screen Reading")
        self.toggle_button.clicked.connect(self.toggle_reading)
        layout.addWidget(self.toggle_button)

        self.acquire_button = QPushButton("Acquire Data")
        self.acquire_button.clicked.connect(
            lambda: self.run_with_feedback(
                self.experiment.acquire_data,
                "Data acquired"
            )
        )
        layout.addWidget(self.acquire_button)

        self.analyse_button = QPushButton("Analyse Data")
        self.analyse_button.clicked.connect(
            lambda: self.run_with_feedback(
                self.experiment.analyse,
                "Analysis complete"
            )
        )
        layout.addWidget(self.analyse_button)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(
            lambda: self.run_with_feedback(
                self.experiment.plot,
                "Graph generated"
            )
        )
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

        if self.reading_enabled:
            self.read_experiment()

    def speak_if_enabled(self, text):

        if self.reading_enabled:
            speak(text, settings["voice"])

    def run_with_feedback(self, func, message):

        try:
            func()
            self.speak_if_enabled(message)

        except Exception:

            traceback.print_exc()

            self.speak_if_enabled(
                "Experiment function not implemented or failed"
            )

    def open_instructions(self):

        if not hasattr(self.experiment, "instructions_file"):
            self.speak_if_enabled("Instructions file not available")
            return

        path = os.path.abspath(self.experiment.instructions_file)

        if os.path.exists(path):

            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            self.speak_if_enabled("Opening full instructions")

        else:

            self.speak_if_enabled("Instructions file not found")

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
            2500,
            lambda: self.speak_if_enabled(
                f"Aim. {self.experiment.aim}. "
                f"Apparatus. {', '.join(self.experiment.apparatus)}. "
                f"Procedure. {', '.join(self.experiment.procedure)}."
            )
        )


app = QApplication(sys.argv)

load_fonts()

window = MainWindow()
window.show()

sys.exit(app.exec())
