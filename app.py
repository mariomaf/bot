from flask import Flask, render_template
import services.InitService as InitService
from services.TokenService import tokenList

app = Flask(__name__)
InitService.InitialiseBot()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/tokens/')
def tokens():
    return render_template("tokens/showtokens.html", tokenList=tokenList)


if __name__ == '__main__':
    app.run()
