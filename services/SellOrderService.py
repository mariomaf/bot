import datetime, json
import entity.sellOrder
import services.InitService as InitService
from pathlib import Path


def placeVirtualSellOrder():
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Creating Virtual SellOrder #####")


def swapToSellOrder(buyOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Swapping Buy Order to Sell Order #####")
    # TODO: fetch takeprofit from tradingpairs.json
    # TODO: also include temporarily the buyorder being swapped and later the actual swapped order details along with the sell order
    tp = 0.05
    sellOrder = entity.sellOrder.SellOrder(buyOrder.swapToken,                  # The swaptoken from buy becomes basetoken
                                        buyOrder.baseToken,                     # The basetoken from buy becomes swaptoken
                                        buyOrder.buyprice,                      #
                                        float(buyOrder.buyprice) * (1 + tp),    # sell price
                                        buyOrder.amountSwapped,                 # amount swapped in buy order expressed in base token of sell order
                                        float(buyOrder.amountSwapped) * float(buyOrder.buyprice) * (1 + tp),     # Swapped amount after sell express in swap token
                                        float(buyOrder.buyprice) * (1 + tp) - float(buyOrder.buyprice),                               # expected profit
                                        tp * 100)            #
    write_json(sellOrder)

# function to add a sellOrder to the JSON
def write_json(sellOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Add new sell order to outstanding Sell Orders #####")
    # First fetch the list of outstanding SellOrders
    sellOrderList = fetchSellOrders(InitService.sell_orders_file_location)
    # now append the new sellOrder
    sellOrderList = addSellOrderToList(sellOrderList, sellOrder)
    # now convert from quote entity list to JSON object
    sellOrderJSON = json.dumps(sellOrderList, ensure_ascii=False, default=lambda o: o.__dict__,
                           sort_keys=False, indent=4)
    with open(InitService.getSellOrdersFileLocation(), 'w+') as json_file:
        json_file.write(sellOrderJSON + '\n')

def fetchSellOrders(filename):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Fetching outstanding Sell Orders #####")
    if checkIfFileExists(filename):
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

# TODO : Make this a common service
def checkIfFileExists(filename):
    my_file = Path(filename)
    if my_file.is_file():
        return True
    else:
        return False

def fetchSellOrderList():
    with open(InitService.getSellOrdersFileLocation()) as json_file:
        JSONFromFile = json.load(json_file)
        sellOrderList = convertToList(JSONFromFile)
        return sellOrderList

def fetchSellOrdersToSwap(quoteResponseList):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Fetch SellOrders to SWAP #####")
    # Validate if an outstanding virtual sell order is smaller then recent quote
    modifiedSellOrderlist = []
    closedSellOrderList = [] # TODO : REMOVE no longer needed
    for quoteResponse in quoteResponseList:
        for sellOrder in fetchSellOrderList():
            print(sellOrder)
            if float(sellOrder.sellprice) < float(quoteResponse.toAmount):
                print(datetime.datetime.now().isoformat() + " ##### SellOrderService: !!HIT!! Quote price [[" + str(
                    quoteResponse.toAmount) + "]] is higher Virtual Sell Order price [[" + str(
                    sellOrder.sellprice) + "]] for pair <BTSBUSD> #####")
                closedSellOrderList.append(sellOrder) # TODO : REMOVE no longer needed
                appendClosedSwapToFile(sellOrder)
            else:
                print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Quote price [[" + str(
                    quoteResponse.toAmount) + "]] is lower than Virtual Sell Order price [[" + str(
                    sellOrder.sellprice) + "]] for pair <BTSBUSD> #####")
                # SellOrder remains valid therefore appended to the ModifiedSellOrderList
                modifiedSellOrderlist.append(sellOrder)
        print(closedSellOrderList)
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

# TODO : Make this a common service
def fetchClosedSwaps(filename):
    if checkIfFileExists(filename):
        with open(filename) as json_file:
            JSONFromFile = json.load(json_file)
            # create list of quotes from json file
            closedSwapList = convertToList(JSONFromFile)
            return closedSwapList
    else:
        closedSwapList = []
        return closedSwapList

# TODO : Make this a common service
def checkIfFileExists(filename):
    my_file = Path(filename)
    if my_file.is_file():
        return True
    else:
        return False

# function to add a new closed swap to an existing List of Closed Sell Order Objects
def addClosedSwapToList(closedSwapList, closedSwap):
    # append the quote entity object to the quoteList
    closedSwapList.append(closedSwap)
    return closedSwapList