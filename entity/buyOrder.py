import json, datetime

# Add max buy price as parameter
class BuyOrder:
    ''' This is the BuyOrder Class '''
    def __init__(self, baseToken, swapToken, buyprice, amount, amountSwapped, lastpricequote, distancepercentage, dateTimeStamp=None):
        self.baseToken = baseToken
        self.swapToken = swapToken
        self.buyprice = buyprice
        self.amount = amount
        self.amountSwapped = amountSwapped
        self.lastpricequote = lastpricequote
        self.distancepercentage = distancepercentage
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)