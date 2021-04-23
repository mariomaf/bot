from pathlib import Path


def checkIfFileExists(filename):
    my_file = Path(filename)
    if my_file.is_file():
        return True
    else:
        return False