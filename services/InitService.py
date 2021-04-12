import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
import services.ProtocolService as ProtocolService
import json
import services.BackGroundTaskService as backGroundService

quote_file_location = ''
buy_order_file_location = ''
quote_interval = ''
quote_history_count = ''
buy_order_interval = ''


def InitialiseBot():
    ReadConfigFile()
    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()
    ProtocolService.getProtocols()
    backGroundService.startBackGroundTasks()


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