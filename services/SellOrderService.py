import datetime, json
import entity.sellOrder
import services.InitService as InitService
from pathlib import Path
import services.TradingPairService as tradingPairService
import services.CommonServices as commonService


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
                                                    sellOrder["quote"],
                                                    sellOrder["buyOrder"],
                                                    sellOrder["UUID"],
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
                appendClosedSwapToFile(sellOrder, quoteResponse)
            else:
                print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Quote price [[" + str(
                    quoteResponse.toAmount) + "]] is lower than Virtual Sell Order price [[" + str(
                    sellOrder.sellprice) + "]] for pair <BTSBUSD> #####")
                # SellOrder remains valid therefore appended to the ModifiedSellOrderList
                modifiedSellOrderlist.append(sellOrder)
        commonService.writeJson(InitService.getSellOrdersFileLocation(), modifiedSellOrderlist)
        # write_json2(modifiedSellOrderlist, InitService.getSellOrdersFileLocation())
        # appendClosedSwapToFile(closedSellOrderList)

def appendClosedSwapToFile(closedSellOrder, quoteResponse):
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


def placeVirtualSellOrder(swapOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Swapping Buy Order to Sell Order #####")
    buyOrder = swapOrder.order
    quoteResponse = swapOrder.quote
    # TODO: also include temporarily the buyorder being swapped and later the actual swapped order details along with the sell order
    # TODO: include slippage
    tp = tradingPairService.FetchTradingPairs()[0].takeProfitPercentage
    sellOrder = entity.sellOrder.SellOrder(buyOrder.swapToken,  # The swaptoken from buy becomes basetoken
                                        buyOrder.baseToken, # The basetoken from buy becomes swaptoken
                                        quoteResponse.toAmount,  # Price for which the amount of basetoken was purchased, for now this is the quoted price
                                        float(quoteResponse.toAmount) * (1 + tp / 100),  # sell price based on quoted price later based on real swap
                                        buyOrder.amount / quoteResponse.toAmount, # amount swapped in buy order expressed in base token of sell order
                                        buyOrder.amount / quoteResponse.toAmount * float(quoteResponse.toAmount) * (1 + tp / 100), # Swapped amount if sell order would be filled
                                        buyOrder.amount / quoteResponse.toAmount * float(quoteResponse.toAmount) * (1 + tp / 100) - buyOrder.amount, # expected profit
                                        tp,            # Take profit percentage
                                        quoteResponse,
                                        buyOrder)
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Add new sell order to outstanding Sell Orders #####")
    # First fetch the list of outstanding SellOrders
    sellOrderList = fetchSellOrders()
    # now append the new sellOrder
    sellOrderList = addSellOrderToList(sellOrderList, sellOrder)
    # now convert from quote entity list to JSON object
    commonService.writeJson(InitService.getSellOrdersFileLocation(), sellOrderList)