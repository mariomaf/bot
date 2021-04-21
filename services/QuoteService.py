import services.TradingPairService as tradingPairService
import services.BuyOrderService as buyOrderService
import services.SellOrderService as sellOrderService
import entity.quoteRequest, requests, json
import entity.quoteResponse
import services.TokenService
from pathlib import Path
import services.InitService as InitService
import datetime


def ScheduledQuoteRequest():
    print(datetime.datetime.now().isoformat() + " ##### QuoteService: Renewing quotes #####")
    # Create for each of the pairs a quoteRequest Entity and add to quoteRequestList
    quoteRequestList = []
    tradingPairList = tradingPairService.FetchTradingPairs()
    for tradingPair in tradingPairList:
        quoteRequest = entity.quoteRequest.QuoteRequest(tradingPair.get_baseToken(), tradingPair.get_swapToken(), 1,
                                                        tradingPair.get_pathPreferred(),
                                                        tradingPair.get_baseTokenAddress(),
                                                        tradingPair.get_swapTokenAddress(),
                                                        tradingPair.get_pathPreferred())
        quoteRequestList.append(quoteRequest)
    quoteResponseList = getQuotes(quoteRequestList)
    buyOrderService.checkBuyOrdersForExecution(quoteResponseList)
    sellOrderService.fetchSellOrdersToSwap(quoteResponseList)
    print(datetime.datetime.now().isoformat() + " ##### QuoteService: Quotes successfully renewed #####")


def getQuotes(quoteRequestList):
    quoteResponseList = []

    for quoteRequest in quoteRequestList:

        if quoteRequest.path == "PANCAKESWAP":
            # TODO: make request url base a config url
            # TODO: amount dynamic in url
            requestUrl = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quotes?deepLevel=2&mainRouteParts=10&parts=20&virtualParts=20&fromTokenAddress=' + quoteRequest.fromAddress + '&toTokenAddress=' + quoteRequest.toAddress + '&amount=1000000000000000000&gasPrice=10000000000&protocolWhiteList=' + quoteRequest.path + '&protocols=' + quoteRequest.path + '&deepLevels=1&mainRoutePartsList=1&partsList=1&virtualPartsList=1'
            r = requests.get(requestUrl)
            if r.status_code == 200:
                quoteResponse = json.loads(r.content)
                quoteResponseList.append(convertQuoteResponseReceived(quoteResponse, 'pathfinder1inch'))
            if r.status_code == 500:
                # TODO: implement proper exception logging
                print("Exception (500) while fetching quote for protocol " + protocol.name)
            if r.status_code == 400:
                # TODO: implement proper exception logging
                print("Exception (400) while fetching quote for protocol " + protocol.name)
    return quoteResponseList


# Function that converts the QuoteResponseDTO into a generic QuoteResponse Object
def convertQuoteResponseReceived(quoteResponseDTO, apiprotocol):
    # TODO make this a generic function that calls a specific mapper
    # TODO make a switch whether or not to purely convert a quote or to fully process a quoteresponse (eg. persisting in JSON FILE)
    if apiprotocol == 'pathfinder1inch':
        fromAddress = quoteResponseDTO['bestResult']['routes'][0]['subRoutes'][0][0]['fromTokenAddress']
        fromSymbol = services.TokenService.getTicker(fromAddress)
        toAddress = quoteResponseDTO['bestResult']['routes'][0]['subRoutes'][0][0]['toTokenAddress']
        toSymbol = services.TokenService.getTicker(toAddress)
        fromTokenAmount = 1
        toTokenAmount = int(quoteResponseDTO['bestResult']['toTokenAmount']) / 1000000000000000000
        path = quoteResponseDTO['bestResult']['routes'][0]['subRoutes'][0][0]['market']['name']
        quoteResponseEntity = entity.quoteResponse.QuoteResponse(fromSymbol, toSymbol, fromTokenAmount, toTokenAmount,
                                                                 path, fromAddress, toAddress)
        write_json(quoteResponseEntity)
    return quoteResponseEntity


# function to add a quote to the JSON with historical quotes
def write_json(quoteResponseEntity):
    # First fetch the history of quotes
    quoteList = fetchQuoteResponse(InitService.quote_file_location)
    # Now append the new quote
    quoteList = addQuoteToList(quoteList, quoteResponseEntity)
    # Now convert from quote entity list to JSON object
    quoteJSON = json.dumps(quoteList, ensure_ascii=False, default=lambda o: o.__dict__,
                           sort_keys=False, indent=4)
    with open(InitService.getQuoteFileLocation(), 'w+') as json_file:
        json_file.write(quoteJSON + '\n')

# TODO : Make this a common service
def checkIfFileExists(filename):
    my_file = Path(filename)
    if my_file.is_file():
        return True
    else:
        return False


def fetchRecentQuotes(number):
    # TODO : if the list grows overtime -number might be getting slower, then first reverse the list and then take the first 5 elements
    quoteList = list(reversed(fetchQuoteResponse(InitService.quote_file_location)[-number:]))
    return quoteList


def fetchQuoteResponse(filename):
    if checkIfFileExists(filename):
        with open(filename) as json_file:
            JSONFromFile = json.load(json_file)
            # create list of quotes from json file
            quoteList = convertToList(JSONFromFile)
            return quoteList
    else:
        quoteList = []
        return quoteList


# function that converts JSON with quotesReceived into list of quote entity objects
def convertToList(quoteJSON):
    quoteList = []
    for quote in quoteJSON:
        # convert each quote to a quote entity object
        quoteToAdd = entity.quoteResponse.QuoteResponse(quote["fromToken"], quote["toToken"], quote["fromAmount"],
                                                        quote["toAmount"], quote["path"], quote["fromAddress"],
                                                        quote["toAddress"], quote["dateTimeStamp"])
        # now add the entity object to the list
        quoteList.append(quoteToAdd)
    return quoteList


# function to add a new quote to an existing List of Quote Objects
def addQuoteToList(quoteList, quoteResponseEntity):
    # append the quote entity object to the quoteList
    quoteList = quoteList[-InitService.getQuoteHistoryCount():]
    quoteList.append(quoteResponseEntity)
    return quoteList
