import json
import entity.tradingPair

tradingPairList = []


def FetchTradingPairs():
    # Fetch a list of trading pairs for which quotes should be fetched
    with open('tradingpairs.json') as json_file:
        JSONFromFile = json.load(json_file)
        tradingPairList = ConvertToList(JSONFromFile)
        return tradingPairList

def ConvertToList(tradingPairJSON):
    tradingPairList = []
    for tradingPairFromJSON in tradingPairJSON:
        # convert each trading pair to a trading pair entity object
        tradingPairToAdd = entity.tradingPair.TradingPair(tradingPairFromJSON["baseToken"],
                                                    tradingPairFromJSON["swapToken"],
                                                    tradingPairFromJSON["moonBagPercentage"],
                                                    tradingPairFromJSON["allocationPercentage"],
                                                    tradingPairFromJSON["takeProfitPercentage"],
                                                    tradingPairFromJSON["minimumOrderSize"],
                                                    tradingPairFromJSON["pathPreferred"],
                                                    tradingPairFromJSON['maxOutstandingBuyOrders'],
                                                    tradingPairFromJSON["slippage"],
                                                    tradingPairFromJSON["baseTokenAddress"],
                                                    tradingPairFromJSON["swapTokenAddress"],
                                                    tradingPairFromJSON["dateTimeStamp"])
        # now add the entity object to the list
        tradingPairList.append(tradingPairToAdd)
    return tradingPairList