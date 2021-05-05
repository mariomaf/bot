import entity.token as token, json, requests

# creating list
tokenList = []

# This function is used to fetch the actual tokenlist and this runs on initialization of this bot
def getTokens():
    # fetch all tokens
    r = requests.get('https://api.1inch.exchange/v3.0/56/tokens')
    data = json.loads(r.content)

    # create list of token objects
    for key, value in data['tokens'].items():
        tokenList.append(token.Token(value['name'], value['symbol'], value['address'], value['decimals']))

# Get full tokenlist
def getTokenList():
    return tokenList

# Get the specific ticker based on address
def getTicker(address):
    # Find dictionary matching value in list
    for token in tokenList:
        if token.address == address:
            ticker = token.ticker
    return ticker

def getDecimals(address):
    # Find dictionary matching value in list
    decimals = 18
    for token in tokenList:
        if token.address == address:
            decimals = token.decimals
    return decimals

def getAddress(ticker):
    # Find dictionary matching value in list
    decimals = 18
    for token in tokenList:
        if token.ticker == ticker:
            address = token.address
    return address