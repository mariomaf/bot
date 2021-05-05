import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
import services.ProtocolService as ProtocolService
import services.BuyOrderService as BuyOrderService
import services.SellOrderService as SellOrderService
import services.TradeService as TradeService
import services.QuoteService as QuoteService
import json, datetime, requests
import services.BackGroundTaskService as backGroundService

quote_file_location = ''
buy_order_file_location = ''
sell_orders_file_location = ''
quote_interval = ''
quote_history_count = ''
buy_order_interval = ''
trading_pairs_file_location = ''
results_file_location = ''
closedswaps_file_location = ''
keys = {}


def InitialiseBot():
    print(datetime.datetime.now().isoformat() + " ##### InitService: Initialising Bot #####")
    ReadConfigFile()
    ImportKeys()
    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()
    ProtocolService.getProtocols()
    backGroundService.startBackGroundTasks()
    print(datetime.datetime.now().isoformat() + " ##### InitService: Bot is initialised #####")

def RestartBot():
    print(datetime.datetime.now().isoformat() + " ##### InitService: Restarting bot #####")
    backGroundService.restartEngine()
    print(datetime.datetime.now().isoformat() + " ##### InitService: Bot restarted #####")

def ImportKeys(filename="keys.json"):
    try:
        with open(filename) as json_file:
            global keys
            keys = json.load(json_file)
    except:
        print(print(datetime.datetime.now().isoformat() + " ##### InitService: keys.json import failed #####"))


def ReadConfigFile(filename="config.json"):
    with open(filename) as json_file:
        config = json.load(json_file)
    global quote_file_location
    quote_file_location = config["quote_file_location"]
    global buy_order_file_location
    buy_order_file_location = config["buy_orders_file_location"]
    global quote_interval
    quote_interval = config["quote_interval"]
    global quote_history_count
    quote_history_count = config["quote_history_count"]
    global buy_order_interval
    buy_order_interval = config["buy_order_interval"]
    global trading_pairs_file_location
    trading_pairs_file_location = config["trading_pairs_file_location"]
    global sell_orders_file_location
    sell_orders_file_location = config["sell_orders_file_location"]
    global results_file_location
    results_file_location = config["results_file_location"]
    global closed_swaps_file_location
    closed_swaps_file_location = config["closed_swaps_file_location"]
    global tradeExecution
    tradeExecution = config["tradeExecution"]


def getQuoteFileLocation():
    return quote_file_location

def getBuyOrderFileLocation():
    return buy_order_file_location

def getQuoteInterval():
    return quote_interval

def getQuoteHistoryCount():
    return quote_history_count

def getBuyOrderInterval():
    return buy_order_interval

def getTradingPairsFileLocation():
    return trading_pairs_file_location

def getSellOrdersFileLocation():
    return sell_orders_file_location

def getResultsFileLocation():
    return results_file_location

def getClosedSwapsFileLocation():
    return closed_swaps_file_location

def getTradeExecution():
    return tradeExecution


# TODO: Add Sell Order File Location, Results File Location, ClosedSwaps file location to DashBoardFigures
def getDashBoardFigures():
    dashBoardFigures = {"buy_order_interval" : buy_order_interval,
                        "quote_interval" : quote_interval,
                        "quote_history_count" : quote_history_count,
                        "quote_file_location" : quote_file_location,
                        "buy_order_file_location" : buy_order_file_location,
                        "quote_history_count" : quote_history_count,
                        "trading_pairs_file_location" : trading_pairs_file_location,
                        "trading_pairs" : TradingPairService.FetchTradingPairs(),
                        "buy_orders" : BuyOrderService.fetchBuyOrderList(),
                        "sell_orders" : SellOrderService.fetchSellOrders(),
                        "closed_trades": TradeService.fetchClosedTradeList(),
                        "last_quotes" : QuoteService.fetchRecentQuotes(1),
                        "status_exchange" : requests.get('https://api.1inch.exchange/v3.0/56/healthcheck').json()["status"],
                        "public_key" : keys["public"],
                        "tradeExecution" : getTradeExecution()}
    return dashBoardFigures