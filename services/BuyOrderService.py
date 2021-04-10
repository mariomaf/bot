import services.TradingPairService as tradingPairService
import services.QuoteService as quoteService
import entity.buyOrder
import json
import services.InitService as InitService

# This function is triggered via an API by a scheduler in order to calculate the buy orders based on the pair settings
def placeVirtualBuyorders():
    # Fetch a list of trading pairs for which quotes should be fetched
    tradingPairList = tradingPairService.FetchTradingPairs()
    # now loop trough the list of tradingPair objects
    outStandingBuyOrderList = []

    for tradingPair in tradingPairList:
        lastQuoteResponses = quoteService.fetchRecentQuotes(1)
        buyOrderPairList = calculateBuyOrderList(lastQuoteResponses, tradingPair)
        pair = tradingPair.swapToken + tradingPair.baseToken
        pairToAdd = {}
        pairToAdd[pair] = {}
        pairToAdd[pair] = buyOrderPairList
        outStandingBuyOrderList.append(pairToAdd)
    # Now actualise the buyOrderList JSON file
    write_json(outStandingBuyOrderList)
    # TODO: Return full list, not only actualised ones but also ones for which no pair is active
    return outStandingBuyOrderList


def calculateBuyOrderList(recentQuoteList, tradingPair):
    # take the relevant trading pair parameters

    buyOrderList = []
    minimumDistancePercentage = 2
    #quotedToAmount = float(recentQuoteList[0]["toAmount"])
    quotedToAmount = [o.toAmount for o in recentQuoteList]
    for x in range(0, tradingPair.maxOutstandingBuyOrders):
        # TODO minimumDistancePercentage move to tradingPair entity
        # TODO calculate free allocation available for the base token
        pricingFactor = (100 - minimumDistancePercentage) * (1 - (1 + x * 1) / 100)
        buyPrice = quotedToAmount[0] * pricingFactor / 100
        amount = 100
        amountSwapped = amount / buyPrice
        # In the loop this should chance per loop
        buyOrder = entity.buyOrder.BuyOrder(tradingPair.baseToken,
                                            tradingPair.swapToken,
                                            str(round(buyPrice,5)),
                                            amount,
                                            str(round(amountSwapped, 5)),
                                            str(round(quotedToAmount[0], 5)),
                                            str(round(pricingFactor, 2)))
        buyOrderList.append(buyOrder)

    return buyOrderList

def write_json(outstandingBuyOrderList, filename=InitService.getBuyOrderFileLocation()):
    buyOrderListDTO = json.dumps(outstandingBuyOrderList, ensure_ascii=False, default=lambda o: o.__dict__,
               sort_keys=False, indent=4)
    with open(InitService.getBuyOrderFileLocation(), 'w') as json_file:
        json_file.write(buyOrderListDTO + '\n')

def fetchBuyOrderList():
    with open('data_buyorders.json') as json_file:
        JSONFromFile = json.load(json_file)
        buyOrderList = ConvertToList(JSONFromFile)
        return buyOrderList

def ConvertToList(BuyOrderListDTO):
    print(BuyOrderListDTO)
    buyOrderList = []
    return buyOrderList
