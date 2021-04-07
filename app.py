from flask import Flask, render_template
import services.InitService as InitService
from services.TokenService import tokenList
from services.ProtocolService import protocolList

app = Flask(__name__)
InitService.InitialiseBot()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tokens/')
def tokens():
    return render_template("tokens/showtokens.html", tokenList=tokenList)

@app.route('/protocols')
def protocols():
    return render_template("protocols/protocols.html", protocolList=protocolList)


if __name__ == '__main__':
    app.run()
