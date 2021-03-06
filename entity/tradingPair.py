import datetime, json

# TODO: add min buy price
class TradingPair:
    ''' This is the TradingPair Class '''
    def __init__(self, baseToken, swapToken, moonBagPercentage, allocationPercentage, takeProfitPercentage, minimumDistance, minimumOrderSize, maxBuyPrice, pathPreferred, maxOutstandingBuyOrders, slippage, baseTokenAddress, swapTokenAddress, dateTimeStamp):
        self.baseToken = baseToken
        self.swapToken = swapToken
        self.moonBagPercentage = moonBagPercentage
        self.allocationPercentage = allocationPercentage
        self.takeProfitPercentage = takeProfitPercentage
        self.minimumDistance = minimumDistance
        self.minimumOrderSize = minimumOrderSize
        self.maxBuyPrice = maxBuyPrice
        self.pathPreferred = pathPreferred
        self.maxOutstandingBuyOrders = maxOutstandingBuyOrders
        self.slippage = slippage
        self.baseTokenAddress = baseTokenAddress
        self.swapTokenAddress = swapTokenAddress
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)

    def get_baseToken(self):
        return self.baseToken

    def get_swapToken(self):
        return self.swapToken

    def get_moonBagPercentage(self):
        return self.moonBagPercentage

    def get_allocationPercentage(self):
        return self.allocationPercentage

    def get_takeProfitPercentage(self):
        return self.takeProfitPercentage

    def get_minimumOrderSize(self):
        return self.minimumOrderSize

    def get_pathPreferred(self):
        return self.pathPreferred

    def get_baseTokenAddress(self):
        return self.baseTokenAddress

    def get_swapTokenAddress(self):
        return self.swapTokenAddress

    def get_dateTimeStamp(self):
        return self.dateTimeStamp

    def get_minimumDistance(self):
        return self.minimumDistance

    def get_maxBuyPrice(self):
        return self.maxBuyPrice