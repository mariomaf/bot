import services.InitService as initService
import entity.sellOrder
import json

def fetchClosedTradeList():
    with open(initService.getClosedSwapsFileLocation()) as json_file:
        JSONFromFile = json.load(json_file)
        closedSwapList = convertToList(JSONFromFile)
        print(closedSwapList)
        return closedSwapList


def convertToList(closedSwapJSON):
    print(closedSwapJSON)
    closedSwapList = []
    for closedSwap in closedSwapJSON:
        # convert each closed Swap to a closeSwap entity object
        closedSwapTradeToAdd = entity.sellOrder.SellOrder(closedSwap["baseToken"],
                                                    closedSwap["swapToken"],
                                                    closedSwap["buyprice"],
                                                    closedSwap["sellprice"],
                                                    closedSwap["amount"],
                                                    closedSwap["amountSwapped"],
                                                    closedSwap["expectedprofit"],
                                                    closedSwap["takeprofitpercentage"],
                                                    closedSwap["dateTimeStamp"])
        # now add the entity object to the list
        closedSwapList.append(closedSwapTradeToAdd)
    return closedSwapList