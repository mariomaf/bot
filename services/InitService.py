import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
import services.ProtocolService as ProtocolService
import json

quote_file_location = ''


def InitialiseBot():
    ReadConfigFile()
    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()
    ProtocolService.getProtocols()


def ReadConfigFile(filename="config.json"):
    with open(filename) as json_file:
        config = json.load(json_file)
    global quote_file_location
    quote_file_location = config["quote_file_location"]


def getQuoteFileLocation():
    return quote_file_location
