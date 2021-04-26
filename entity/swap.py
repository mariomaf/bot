import json, datetime

class Swap:
    ''' This is the Swap Class '''
    # TODO: Add protocol, ?
    def __init__(self, baseToken, swapToken, price, baseAmount, swappedAmount, type,
                 slippage, order, quote, dateTimeStamp=None):
        self.baseToken = baseToken
        self.swapToken = swapToken
        self.price = price
        self.baseAmount = baseAmount # This is the amount of baseToken to be swapped in swapToken
        self.swappedAmount = swappedAmount # Expected amount after swap expressed in swapToken
        self.type = type # Either BUY or SELL
        self.slippage = slippage
        self.order = order
        self.quote = quote
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)