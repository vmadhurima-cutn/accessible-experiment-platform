import platform
import subprocess

SYSTEM = platform.system()


def speak(text, voice=None):

    if SYSTEM == "Darwin":

        command = ["say"]

        if voice:
            command += ["-v", voice]

        command.append(text)
        subprocess.Popen(command)


    elif SYSTEM == "Linux":

        command = ["espeak"]

        if voice:
            command += ["-v", voice]

        command.append(text)
        subprocess.Popen(command)


    elif SYSTEM == "Windows":

        script = f'''
Add-Type –AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Speak("{text}")
'''

        subprocess.Popen(["powershell", "-Command", script])


def get_voices():

    if SYSTEM == "Darwin":

        result = subprocess.run(
            ["say", "-v", "?"], capture_output=True, text=True
        )

        voices = []

        for line in result.stdout.splitlines():

            parts = line.split()

            if len(parts) >= 2:
                voices.append(parts[0])

        return voices


    elif SYSTEM == "Linux":

        # common espeak voices
        return [
            "en", "en-us", "en-scotland",
            "en-westindies"
        ]


    elif SYSTEM == "Windows":

        # Windows voices are accessed through SAPI
        return ["Default"]