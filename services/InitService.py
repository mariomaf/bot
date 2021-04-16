import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
import services.ProtocolService as ProtocolService
import services.BuyOrderService as BuyOrderService
import services.QuoteService as QuoteService
import json, datetime
import services.BackGroundTaskService as backGroundService

quote_file_location = ''
buy_order_file_location = ''
quote_interval = ''
quote_history_count = ''
buy_order_interval = ''
trading_pairs_file_location = ''


def InitialiseBot():
    print(datetime.datetime.now().isoformat() + " ##### InitService: Initialising Bot #####")
    ReadConfigFile()
    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()
    ProtocolService.getProtocols()
    backGroundService.startBackGroundTasks()
    print(datetime.datetime.now().isoformat() + " ##### InitService: Bot is initialised #####")


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
                        "last_quotes" : QuoteService.fetchRecentQuotes(1)}
    return dashBoardFigures