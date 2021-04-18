import datetime, json
import entity.sellOrder
import services.InitService as InitService
from pathlib import Path


def placeVirtualSellOrder():
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Creating Virtual SellOrder #####")


def swapToSellOrder(buyOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Swapping Buy Order to Sell Order #####")
    # TODO: fetch takeprofit from tradingpairs.json
    tp = 0.05
    sellOrder = entity.sellOrder.SellOrder(buyOrder.swapToken,                  # The swaptoken from buy becomes basetoken
                                        buyOrder.baseToken,                     # The basetoken from buy becomes swaptoken
                                        buyOrder.buyprice,                      #
                                        float(buyOrder.buyprice) * (1 + tp),    # sell price
                                        buyOrder.amountSwapped,                 #
                                        float(buyOrder.amountSwapped) * tp,     #
                                        float(buyOrder.buyprice) * (1 + tp) - float(buyOrder.buyprice),                               # expected profit
                                        tp * 100)            #
    write_json(sellOrder)

# function to add a sellOrder to the JSON
def write_json(sellOrder):
    print(datetime.datetime.now().isoformat() + " ##### SellOrderService: Add new sell order to outstanding Sell Orders #####")
    # First fetch the list of outstanding SellOrders
    sellOrderList = fetchSellOrders(InitService.sell_orders_file_location)
    print("t1", sellOrderList)
    # now append the new sellOrder
    sellOrderList = addSellOrderToList(sellOrderList, sellOrder)
    # now convert from quote entity list to JSON object
    print("t2", sellOrderList)
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