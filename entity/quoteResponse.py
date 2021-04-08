import datetime, json

class QuoteResponse:
    ''' This is the QuoteResponse Class '''
    def __init__(self, fromToken, toToken, fromAmount, toAmount, path, fromAddress, toAddress, dateTimeStamp=None):
        self.fromToken = fromToken
        self.toToken = toToken
        self.fromAmount = fromAmount
        self.toAmount = toAmount
        self.path = path
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)