import services.TradingPairService as tradingPairService
import services.QuoteService as quoteService
import entity.buyOrder
import json, datetime
import services.InitService as InitService
import services.SellOrderService as SellOrderService


# This function is triggered via an API by a scheduler in order to calculate the buy orders based on the pair settings
def placeVirtualBuyorders():
    print(datetime.datetime.now().isoformat() + " ##### BuyOrderService: Actualising BuyOrderList #####")
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
    print(datetime.datetime.now().isoformat() + " ##### BuyOrderService: BuyOrderList actualised #####")
    # TODO: Return full list, not only actualised ones but also ones for which no pair is active
    return outStandingBuyOrderList


def calculateBuyOrderList(recentQuoteList, tradingPair):
    # take the relevant trading pair parameters

    buyOrderList = []
    minimumDistancePercentage = 2
    # quotedToAmount = float(recentQuoteList[0]["toAmount"])
    quotedToAmount = [o.toAmount for o in recentQuoteList]
    for x in range(0, tradingPair.maxOutstandingBuyOrders):
        # TODO calculate free allocation available for the base token
        pricingFactor = (100 - tradingPairService.fetchTradingPairSetting("BUSD", "BTS", "minimumDistance")) * (1 - (1 + x * 1) / 100)
        buyPrice = quotedToAmount[0] * pricingFactor / 100
        amount = 100
        amountSwapped = amount / buyPrice
        # In the loop this should chance per loop
        buyOrder = entity.buyOrder.BuyOrder(tradingPair.baseToken,
                                            tradingPair.swapToken,
                                            str(round(buyPrice, 5)),
                                            amount,
                                            str(round(amountSwapped, 5)),
                                            str(round(quotedToAmount[0], 5)),
                                            str(round(pricingFactor, 2)))
        buyOrderList.append(buyOrder)

    return buyOrderList


def write_json(outstandingBuyOrderList):
    buyOrderListDTO = json.dumps(outstandingBuyOrderList, ensure_ascii=False, default=lambda o: o.__dict__,
                                 sort_keys=False, indent=4)
    with open(InitService.getBuyOrderFileLocation(), 'w') as json_file:
        json_file.write(buyOrderListDTO + '\n')


def fetchBuyOrderList():
    with open(InitService.getBuyOrderFileLocation()) as json_file:
        JSONFromFile = json.load(json_file)
        buyOrderList = ConvertToList(JSONFromFile)
        return buyOrderList


def ConvertToList(BuyOrderListDTO):
    buyOrderList = []
    for BuyOrderListPairDTO in BuyOrderListDTO:
        for key in BuyOrderListPairDTO.keys():
            pair = key
            # Now iterate through the buy orders and convert all the buy orders to a buy order entity which will be added to the list
            outStandingBuyOrderPairList = []
            for outStandingBuyOrderDTO in BuyOrderListPairDTO[pair]:
                # Create a buy order entity
                buyOrder = entity.buyOrder.BuyOrder(outStandingBuyOrderDTO["baseToken"],
                                                    outStandingBuyOrderDTO["swapToken"],
                                                    outStandingBuyOrderDTO["buyprice"],
                                                    outStandingBuyOrderDTO["amount"],
                                                    outStandingBuyOrderDTO["amountSwapped"],
                                                    outStandingBuyOrderDTO["lastpricequote"],
                                                    outStandingBuyOrderDTO["distancepercentage"],
                                                    outStandingBuyOrderDTO["dateTimeStamp"])
                outStandingBuyOrderPairList.append(buyOrder)

            # now add the outStandingBuyOrderPairList to the buyOrderList (which will include the buy orders for all pairs)
            pairToAdd = {}
            pairToAdd[pair] = {}
            pairToAdd[pair] = outStandingBuyOrderPairList
            buyOrderList.append(pairToAdd)

    return buyOrderList

def checkBuyOrdersForExecution(quoteResponseList):
    print(datetime.datetime.now().isoformat() + " ##### BuyOrderService: Checking if virtual buy orders to swap #####")
    # Validate if an outstanding virtual buy order is greater then recent quote
    for quoteResponse in quoteResponseList:
        for buyOrderListPair in fetchBuyOrderList():
            for pair, buyOrderList in buyOrderListPair.items():     # pair = key; buyOrderList = value
                modifiedBuyOrderlist = []
                for index, buyOrder in enumerate(buyOrderList):
                    if float(buyOrder.buyprice) > float(quoteResponse.toAmount):
                        print(datetime.datetime.now().isoformat() + " ##### BuyOrderService: !!HIT!! Quote price [[" + str(
                            quoteResponse.toAmount) + "]] is below Virtual Buy Order price [[" + str(
                            buyOrder.buyprice) + "]] for pair <" + pair + ">. #####")
                        SellOrderService.swapToSellOrder(buyOrder)
                    else:
                        print(datetime.datetime.now().isoformat() + " ##### BuyOrderService: Quote price [[" + str(
                            quoteResponse.toAmount) + "]] is above Virtual Buy Order price [[" + str(
                            buyOrder.buyprice) + "]] for pair <" + pair + ">. #####")
                        # BuyOrder remains valid therefore appended to the ModifiedBuyOrderList
                        modifiedBuyOrderlist.append(buyOrder)
                # Now replace the buyOrderList with the modifiedBuyOrderList
                buyOrderListPair[pair] = modifiedBuyOrderlist
                # TODO: Can be removed? Next line?
                jsonStr = json.dumps(buyOrderListPair, ensure_ascii=False, default=lambda o: o.__dict__,
                                     sort_keys=False, indent=4)
            newOutStandingBuyOrderList = []
            newOutStandingBuyOrderList.append(buyOrderListPair)
        write_json(newOutStandingBuyOrderList)