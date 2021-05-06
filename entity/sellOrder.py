import json, datetime, uuid


class SellOrder:
    ''' This is the SellOrder Class '''
    def __init__(self, baseToken, swapToken, buyprice, sellprice, amount, amountSwapped, expectedprofit, takeprofitpercentage, slippage, quote, buyOrder, swapOrder, tx_hash, UUID=None, dateTimeStamp=None):
        self.baseToken = baseToken                          # as this is a swap the base and swap tokens are reversed
        self.swapToken = swapToken                          # as this is a swap the base and swap tokens are reversed
        self.buyprice = buyprice                            # This is the price for which the amount was swapped before
        self.sellprice = sellprice                          # This is the sell price trigger
        self.amount = amount                                # This is the amount expressed in the baseToken, being the amountSwapped from a buyOrder
        self.amountSwapped = amountSwapped                  # This is the minimum amount in the swap token (amount * sell price), if full slippage is used
        self.expectedprofit = expectedprofit                # This is minimum take profit if all slippage is used
        self.takeprofitpercentage = takeprofitpercentage
        self.slippage = slippage                            # Slippage percentage as propagated along with the buyorder
        self.quote = quote                                  # The quote as derived via the quote service
        self.buyOrder = buyOrder                            # This is the original buyOrder as placed by the BuyOrderService
        self.swapOrder = swapOrder                          # SWAP Order created
        self.tx_hash = tx_hash                              # Transaction hash as received from the BSC exchange
        self.UUID = UUID if UUID is not None else str(uuid.uuid4())
        self.dateTimeStamp = dateTimeStamp if dateTimeStamp is not None else datetime.datetime.now().isoformat()

    def toJSON(self):
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)