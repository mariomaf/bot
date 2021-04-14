import json
import entity.tradingPair
import services.InitService as initService

tradingPairList = []


def FetchTradingPairs():
    # Fetch a list of trading pairs for which quotes should be fetched
    global tradingPairList
    try:
        if len(tradingPairList) != 0:
            # TODO: Create logging item
            return tradingPairList
        with open(initService.getTradingPairsFileLocation()) as json_file:
            # TODO: Create logging item
            JSONFromFile = json.load(json_file)
            tradingPairList = ConvertToList(JSONFromFile)
            return tradingPairList
    except NameError:
       print("Log: File '" + initService.getTradingPairsFileLocation() + "' does not exist")


def ConvertToList(tradingPairJSON):
    tradingPairList = []
    for tradingPairFromJSON in tradingPairJSON:
        # convert each trading pair to a trading pair entity object
        tradingPairToAdd = entity.tradingPair.TradingPair(tradingPairFromJSON["baseToken"],
                                                    tradingPairFromJSON["swapToken"],
                                                    tradingPairFromJSON["moonBagPercentage"],
                                                    tradingPairFromJSON["allocationPercentage"],
                                                    tradingPairFromJSON["takeProfitPercentage"],
                                                    tradingPairFromJSON["minimumDistance"],
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

def fetchTradingPairSetting(basetoken, swaptoken, parameterKey):
    filtered_list = [tradingPair for tradingPair in FetchTradingPairs() if tradingPair.get_baseToken() == basetoken and tradingPair.get_swapToken() == swaptoken]
    if filtered_list:
        result = filtered_list[-1]
    else:
        result = None
        # TODO: Add to logging
        print("The requested pair is not set up")
    return getattr(result, parameterKey)