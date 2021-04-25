import json, datetime


class SellOrder:
    ''' This is the SellOrder Class '''
    def __init__(self, baseToken, swapToken, buyprice, sellprice, amount, amountSwapped, expectedprofit, takeprofitpercentage, quote, buyOrder, dateTimeStamp=None):
        self.baseToken = baseToken                          # as this is a swap the base and swap tokens are reversed
        self.swapToken = swapToken                          # as this is a swap the base and swap tokens are reversed
        self.buyprice = buyprice                            # This is the price for which the amount was swapped before
        self.sellprice = sellprice                          # This is the sell price trigger
        self.amount = amount                                # This is the amount expressed in the baseToken, being the amountSwapped from a buyOrder
        self.amountSwapped = amountSwapped                  # This is the amount in the swap token (amount * sell price)
        self.expectedprofit = expectedprofit
        self.takeprofitpercentage = takeprofitpercentage
        self.quote = quote                                  # The quote as derived via teh quote service
        self.buyOrder = buyOrder                            # This is the original buyOrder as placed by the BuyOrderService
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)