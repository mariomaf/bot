import json

class Protocol:
    ''' This is the Protocol Class '''
    def __init__(self, name):
        self.name = name

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)