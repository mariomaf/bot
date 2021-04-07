import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
from services.TradingPairService import tradingPairList

def InitialiseBot():

    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()