class Experiment:

    name = "Simple Pendulum"
    category = "Mechanics"

    aim = """
Determine acceleration due to gravity using a simple pendulum.
"""

    apparatus = [
        "Pendulum bob",
        "String",
        "Stand",
        "Timer or Arduino sensor"
    ]

    procedure = [
        "Measure pendulum length",
        "Release pendulum",
        "Measure oscillation period"
    ]

    def acquire_data(self):
        print("Acquire pendulum data")

    def analyse(self):
        print("Analyse pendulum data")

    def plot(self):
        print("Plot pendulum graph")