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
