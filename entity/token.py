import datetime, json

class Token:
    ''' This is the Token Class'''
    def __init__(self, name, ticker, address, decimals, dateTimeStamp=None):
        self.name = name
        self.ticker = ticker
        self.address = address
        self.decimals = decimals
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)