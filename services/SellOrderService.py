import datetime, json
import entity.sellOrder
import services.InitService as InitService
from pathlib import Path
import services.TradingPairService as tradingPairService
import services.CommonServices as commonService


def placeVirtualSellOrder():
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Creating Virtual SellOrder #####")


def swapToSellOrder(buyOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Swapping Buy Order to Sell Order #####")
    # TODO: also include temporarily the buyorder being swapped and later the actual swapped order details along with the sell order
    tp = tradingPairService.FetchTradingPairs()[0].takeProfitPercentage
    sellOrder = entity.sellOrder.SellOrder(buyOrder.swapToken,  # The swaptoken from buy becomes basetoken
                                        buyOrder.baseToken, # The basetoken from buy becomes swaptoken
                                        buyOrder.buyprice,  # Price for which the amount of basetoken was purchased
                                        float(buyOrder.buyprice) * (1 + tp / 100),  # sell price
                                        buyOrder.amountSwapped, # amount swapped in buy order expressed in base token of sell order
                                        float(buyOrder.amountSwapped) * float(buyOrder.buyprice) * (1 + tp / 100),  # Swapped amount after sell expressed in swap token
                                        float(buyOrder.amountSwapped) * float(buyOrder.buyprice) * (1 + tp / 100) - float(buyOrder.buyprice) * float(buyOrder.amountSwapped), # expected profit
                                        #float(buyOrder.buyprice) * (1 + tp / 100) - float(buyOrder.buyprice),   # expected profit
                                        tp)            # Take profit percentage
    write_json(sellOrder)

# function to add a sellOrder to the JSON
def write_json(sellOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Add new sell order to outstanding Sell Orders #####")
    # First fetch the list of outstanding SellOrders
    sellOrderList = fetchSellOrders()
    # now append the new sellOrder
    sellOrderList = addSellOrderToList(sellOrderList, sellOrder)
    # now convert from quote entity list to JSON object
    sellOrderJSON = json.dumps(sellOrderList, ensure_ascii=False, default=lambda o: o.__dict__,
                           sort_keys=False, indent=4)
    with open(InitService.getSellOrdersFileLocation(), 'w+') as json_file:
        json_file.write(sellOrderJSON + '\n')

def fetchSellOrders():
    filename = InitService.getSellOrdersFileLocation()
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Fetching outstanding Sell Orders #####")
    if commonService.checkIfFileExists(filename):
        with open(filename) as json_file:
            JSONFromFile = json.load(json_file)
            # create list of quotes from json file
            sellOrderList = convertToList(JSONFromFile)
            return sellOrderList
    else:
        print(datetime.datetime.now().isoformat() + " ##### SellOrderService: No outstanding sell orders found #####")
        sellOrderList = []
        return sellOrderList


# function that converts JSON with sellOrders into list of sellOrder entity objects
def convertToList(sellOrderJSON):
    sellOrderList = []
    for sellOrder in sellOrderJSON:
        # convert each sellOrder to a sellOrder entity object
        sellOrderToAdd = entity.sellOrder.SellOrder(sellOrder["baseToken"],
                                                    sellOrder["swapToken"],
                                                    sellOrder["buyprice"],
                                                    sellOrder["sellprice"],
                                                    sellOrder["amount"],
                                                    sellOrder["amountSwapped"],
                                                    sellOrder["expectedprofit"],
                                                    sellOrder["takeprofitpercentage"],
                                                    sellOrder["dateTimeStamp"])
        # now add the entity object to the list
        sellOrderList.append(sellOrderToAdd)
    return sellOrderList

# function to add a new sellOrder to an existing List of SellOrder Objects
def addSellOrderToList(sellOrderList, sellOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Adding sellOrder to list #####")
    # append the sellOrder entity object to the sellOrderList
    sellOrderList.append(sellOrder)
    return sellOrderList

def fetchSellOrdersToSwap(quoteResponseList):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Fetch SellOrders to SWAP #####")
    takeprofit = tradingPairService.FetchTradingPairs()[0].takeProfitPercentage
    # Validate if an outstanding virtual sell order is smaller then recent quote
    modifiedSellOrderlist = []
    for quoteResponse in quoteResponseList:
        for sellOrder in fetchSellOrders():
            if float(sellOrder.sellprice) < float(quoteResponse.toAmount):
                print(datetime.datetime.now().isoformat() + " ##### SellOrderService: !!HIT!! Quote price [[" + str(
                    quoteResponse.toAmount) + "]] is higher then Virtual Sell Order price [[" + str(
                    sellOrder.sellprice) + "]] for pair <BTSBUSD> #####")
                appendClosedSwapToFile(sellOrder)
            else:
                print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Quote price [[" + str(
                    quoteResponse.toAmount) + "]] is lower than Virtual Sell Order price [[" + str(
                    sellOrder.sellprice) + "]] for pair <BTSBUSD> #####")
                # SellOrder remains valid therefore appended to the ModifiedSellOrderList
                modifiedSellOrderlist.append(sellOrder)
        write_json2(modifiedSellOrderlist, InitService.getSellOrdersFileLocation())
        # appendClosedSwapToFile(closedSellOrderList)


def write_json2(sellOrderList, fileLocation):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Write to file " + fileLocation + " #####")
    sellOrderListDTO = json.dumps(sellOrderList, ensure_ascii=False, default=lambda o: o.__dict__,
                                 sort_keys=False, indent=4)
    with open(fileLocation, 'w') as json_file:
        json_file.write(sellOrderListDTO + '\n')

def appendClosedSwapToFile(closedSellOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Appending ClosedSellOrder to ClosedSwaps.json #####")
    # First fetch the historical ClosedSwaps from file
    closedSwapList = fetchClosedSwaps(InitService.getClosedSwapsFileLocation())
    # Now append new closedSellOrder
    closedSwapList = addClosedSwapToList(closedSwapList, closedSellOrder)
    # Now convert from quote entity list to JSON object
    closedSwapJSON = json.dumps(closedSwapList, ensure_ascii=False, default=lambda o: o.__dict__,
                           sort_keys=False, indent=4)
    with open(InitService.getClosedSwapsFileLocation(), 'w+') as json_file:
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