import services.TokenService as TokenService
import services.TradingPairService as TradingPairService
import services.ProtocolService as ProtocolService

def InitialiseBot():

    TokenService.getTokens()
    TradingPairService.FetchTradingPairs()
    ProtocolService.getProtocols()
