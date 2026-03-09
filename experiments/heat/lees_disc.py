class Experiment:

    name = "Lee's Disc"
    category = "Heat"

    aim = """
Determine thermal conductivity using Lee's Disc apparatus.
"""

    apparatus = [
        "Lee's Disc apparatus",
        "Steam chamber",
        "Thermometer"
    ]

    procedure = [
        "Heat the metal disc",
        "Record steady temperature",
        "Measure cooling rate"
    ]

    def acquire_data(self):
        print("Acquire temperature data")

    def analyse(self):
        print("Analyse thermal data")

    def plot(self):
        print("Plot cooling curve")