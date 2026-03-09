# Accessible Experiment Platform

## Overview

The Accessible Experiment Platform is a cross-platform laboratory interface designed to make physics experiments accessible to visually impaired and mobility-impaired students.

The system provides:

* Keyboard-driven navigation
* Text-to-speech narration
* Adjustable font sizes
* Voice selection
* Modular experiment architecture
* Support for Arduino-based sensors
* CSV data experiments
* Graphing and analysis

The software runs on:

* macOS
* Linux
* Windows

and is written entirely in Python.

---

# System Architecture

The program has three main layers.

| Layer              | Purpose                          |
| ------------------ | -------------------------------- |
| GUI                | User interface and accessibility |
| Experiment Modules | Individual experiments           |
| Hardware Interface | Arduino sensor communication     |

The application dynamically loads experiments placed in the `experiments` directory.

---

# Folder Structure

```
accessible-experiment-platform
│
├── accessibility
│   └── speech_manager.py
│
├── config
│   └── settings.py
│
├── data
│   └── csv_loader.py
│
├── experiment
│   ├── base_experiment.py
│   └── example_experiment.py
│
├── experiments
│   ├── mechanics
│   │   ├── simple_pendulum.py
│   │   └── torsion_pendulum.py
│   │
│   └── heat
│       └── lees_disc.py
│
├── gui
│   └── main_window.py
│
├── hardware
│   ├── arduino_interface.py
│   └── serial_detection.py
│
├── web
│   ├── server.py
│   └── templates
│       └── index.html
│
├── main.py
├── speech.py
├── run.sh
├── install.sh
└── requirements.txt
```

---

# Installation

## 1 Install Python

Python 3.10 or newer is recommended.

Download from:

https://www.python.org

---

## 2 Install dependencies

From inside the project folder run:

```
bash install.sh
```

or manually:

```
pip install -r requirements.txt
```

---

# Running the Program

From inside the project folder:

```
./run.sh
```

or

```
python main.py
```

---

# Accessibility Features

The platform supports several accessibility tools.

| Feature              | Description                              |
| -------------------- | ---------------------------------------- |
| Keyboard navigation  | Full interface usable without mouse      |
| Screen narration     | Text-to-speech reading of instructions   |
| Adjustable fonts     | Supports low vision users                |
| Voice selection      | Multiple speech voices                   |
| Experiment narration | Aim, apparatus, and procedure read aloud |

---

# Keyboard Shortcuts

| Shortcut       | Function                     |
| -------------- | ---------------------------- |
| Ctrl / Cmd + O | Open experiment              |
| Ctrl / Cmd + R | Read experiment instructions |
| Ctrl / Cmd + A | Acquire data                 |
| Ctrl / Cmd + N | Analyse data                 |
| Ctrl / Cmd + P | Plot graph                   |

---

# Adding New Experiments

Experiments are simple Python modules.

Create a new file inside:

```
experiments/<category>/
```

Example:

```
experiments/mechanics/new_experiment.py
```

Example template:

```python
from experiment.base_experiment import BaseExperiment

class Experiment(BaseExperiment):

    name = "Example Experiment"
    category = "Mechanics"

    aim = "Demonstrate experimental structure."

    apparatus = [
        "Arduino sensor",
        "Support stand",
        "Timer"
    ]

    procedure = [
        "Connect the sensor",
        "Start the program",
        "Record measurements"
    ]

    def acquire_data(self):
        pass

    def analyse(self):
        pass

    def plot(self):
        pass
```

The program will automatically detect new experiments.

---

# Hardware Experiments

Arduino communication is handled by:

```
hardware/arduino_interface.py
```

Sensors can be read through serial communication.

---

# Data Experiments

Experiments using recorded datasets can use:

```
data/csv_loader.py
```

This allows analysis without hardware.

---

# Contributing

Students can contribute by:

* Adding new experiments
* Improving accessibility
* Improving hardware integration
* Adding graphing modules
* Improving documentation

---

# License

This project is intended for educational use in accessible laboratory environments.

---
