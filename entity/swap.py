import json, datetime

class Swap:
    ''' This is the Swap Class '''

    def __init__(self, baseToken, swapToken, price, baseAmount, swappedAmount, type,
                 slippage, dateTimeStamp=None):
        self.baseToken = baseToken
        self.swapToken = swapToken
        self.price = price
        self.baseAmount = baseAmount
        self.swappedAmount = swappedAmount
        self.type = type # Either BUY or SELL
        self.slippage = slippage
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)