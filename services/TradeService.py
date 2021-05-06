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
                                                    closedSwap["swapOrder"],
                                                    closedSwap["tx_hash"],
                                                    closedSwap["UUID"],
                                                    closedSwap["dateTimeStamp"])
        # now add the entity object to the list
        closedSwapList.append(closedSwapTradeToAdd)
    return closedSwapList


def appendClosedSwapToFile(closedSellOrder, quoteResponse):
    print(datetime.datetime.now().isoformat() + " ##### TradeService: Appending ClosedSellOrder to ClosedSwaps.json #####")
    # First fetch the historical ClosedSwaps from file
    closedSwapList = fetchClosedSwaps(initService.getClosedSwapsFileLocation())
    # Now append new closedSellOrder
    closedSwapList = addClosedSwapToList(closedSwapList, closedSellOrder)
    # Now convert from quote entity list to JSON object
    closedSwapJSON = json.dumps(closedSwapList, ensure_ascii=False, default=lambda o: o.__dict__,
                           sort_keys=False, indent=4)
    with open(initService.getClosedSwapsFileLocation(), 'w+') as json_file:
        json_file.write(closedSwapJSON + '\n')

def fetchClosedSwaps(filename):
    if commonService.checkIfFileExists(filename):
        with open(filename) as json_file:
            JSONFromFile = json.load(json_file)
            # create list of quotes from json file
            closedSwapList = convertToList(JSONFromFile)
            return closedSwapList
    else:
        closedSwapList = []
        return closedSwapList

# function to add a new closed swap to an existing List of Closed Sell Order Objects
def addClosedSwapToList(closedSwapList, closedSwap):
    # append the quote entity object to the quoteList
    closedSwapList.append(closedSwap)
    return closedSwapList