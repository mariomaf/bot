from flask import Flask, render_template
import services.InitService as InitService
from services.TokenService import tokenList
from services.ProtocolService import protocolList
import services.QuoteService as quoteService
import services.BuyOrderService as buyOrderService



app = Flask(__name__)
InitService.InitialiseBot()


@app.route('/')
def home():
    return render_template("index.html", dashBoardData = InitService.getDashBoardFigures())

@app.route('/tokens/')
def tokens():
    return render_template("tokens/showtokens.html", tokenList=tokenList)

@app.route('/protocols')
def protocols():
    return render_template("protocols/protocols.html", protocolList=protocolList)

# This API can be used by a scheduler to fetch quotes
@app.route('/schedule/quotes')
def fetchQuotes():
    quoteService.ScheduledQuoteRequest()
    return render_template("index.html")

# This API
@app.route('/quote')
def quotes():
    return render_template("quotes/quote.html", quoteList = quoteService.fetchRecentQuotes(5))

# This API
@app.route('/buyorders')
def buyorders():
    return render_template("buyorders/buyorders.html", buyOrderList = buyOrderService.fetchBuyOrderList())

# This API can be used by a scheduler to calculate buy positions
@app.route('/schedule/placevirtualbuyorders')
def placeVirtualBuyOrders():
    buyOrderService.placeVirtualBuyorders()
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
