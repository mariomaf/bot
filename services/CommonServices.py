from pathlib import Path
import json, datetime


def checkIfFileExists(filename):
    my_file = Path(filename)
    if my_file.is_file():
        return True
    else:
        return False

def writeJson(file, list):
    print(datetime.datetime.now().isoformat() + " ##### CommonService: Write to file " + file + " #####")
    listDTO = json.dumps(list, ensure_ascii=False, default=lambda o: o.__dict__,
                                 sort_keys=False, indent=4)
    with open(file, 'w') as json_file:
        json_file.write(listDTO + '\n')