class Experiment:

    name = "Torsion Pendulum"
    category = "Mechanics"

    aim = """
Determine torsional rigidity using a torsion pendulum.
"""

    apparatus = [
        "Suspension wire",
        "Disc",
        "Timer or Arduino sensor"
    ]

    procedure = [
        "Twist the disc",
        "Release the disc",
        "Measure oscillation period"
    ]

    def acquire_data(self):
        print("Acquire torsion data")

    def analyse(self):
        print("Analyse torsion data")

    def plot(self):
        print("Plot torsion graph")