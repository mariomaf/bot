import services.InitService as initService
import services.CommonServices as commonService
import entity.sellOrder
import json, datetime

def fetchClosedTradeList():
    filename = initService.getClosedSwapsFileLocation()
    if commonService.checkIfFileExists(filename):
        with open(filename) as json_file:
            JSONFromFile = json.load(json_file)
            closedSwapList = convertToList(JSONFromFile)
            return closedSwapList
    else:
        print(datetime.datetime.now().isoformat() + " ##### TradeService: No closed trades found #####")
        closedSwapList = []
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
                                                    closedSwap["quote"],
                                                    closedSwap["buyOrder"],
                                                    closedSwap["UUID"],
                                                    closedSwap["dateTimeStamp"])
        # now add the entity object to the list
        closedSwapList.append(closedSwapTradeToAdd)
    return closedSwapList