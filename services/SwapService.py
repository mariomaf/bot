import entity.swap
import requests, datetime
import services.SellOrderService as sellOrderService
import services.InitService as initService
import services.TokenService as tokenService
from web3 import Web3
import json

# set BSC Provider in order to communicate with BSC chain
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

def swapBuyOrder(buyOrder, quoteResponse):
    # 1. Prepare Swap
    # TODO take slippage from tradingpairs.json
    slippage = 1
    swapOrder = entity.swap.Swap(buyOrder.baseToken,
                            buyOrder.swapToken,
                            quoteResponse.toAmount,
                            buyOrder.amount,
                            buyOrder.amount/quoteResponse.toAmount,
                            "BUY",
                            slippage,
                            buyOrder,
                            quoteResponse)
    executeSwap(swapOrder)

def swapSellOrder(sellOrder, quoteResponse):
    # 1. Prepare Swap
    slippage = 2
    swapOrder = entity.swap.Swap(sellOrder.baseToken,
                                 sellOrder.swapToken,
                                 quoteResponse.toAmount,
                                 sellOrder.amount,
                                 sellOrder.amount / quoteResponse.toAmount,
                                 "SELL",
                                 slippage,
                                 sellOrder,
                                 quoteResponse)
    executeSwap(swapOrder)


def executeSwap(swapOrder):

        # execute health check of exchange API
        if requests.get('https://api.1inch.exchange/v3.0/56/healthcheck').json()["status"] == "OK":
            print(datetime.datetime.now().isoformat() + " ##### SwapService: Exchange health check okey #####")
            # TODO: 2. Check if approved
            # 3. ActualiseQuote
            quote = fetchActualQuote()
            # 4. Request swap
            swapRequest = requestSwap(tokenService.getAddress(swapOrder.baseToken), tokenService.getAddress(swapOrder.swapToken), swapOrder.baseAmount, swapOrder.slippage)
            print(swapRequest["tx"])
            signed_tx = signTx(swapRequest["tx"])
            print(signed_tx)
            if initService.getTradeExecution() == True:
                tx_hash = sendTx(signed_tx)
                print(tx_hash.hex())
            else:
                tx_hash = "NOT SWAPPED - PAPER TRADING"
            # TODO: BB-8 not implemented yet
            # 4. Creat SellOrder
            if swapOrder.type == "BUY":
                signed_tx_json = json.dumps(signed_tx, ensure_ascii=False, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)
                sellOrderService.placeVirtualSellOrder(swapOrder, tx_hash.hex())
            elif swapOrder.type == "SELL":
                print("test temp")
            return
        else:
            print(datetime.datetime.now().isoformat() + " ##### SwapService: Exchange health check NOT Okey, cannot proceed with swap #####")


def ApproveBaseToken(address):
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))
    approve_response = requests.get(
        'https://api.1inch.exchange/v3.0/56/approve/calldata?infinity=true&tokenAddress=' + web3.toChecksumAddress(address)).json()

    nonce = web3.eth.getTransactionCount(initService.keys["public"])

    # TODO: Gas to be calculated to prevent failures
    tx = {
        'nonce' : nonce,
        'to' : approve_response["to"],
        'data' : approve_response["data"],
        'value' : 0,
        'gas' : 44406,
        'gasPrice' : web3.toWei('5', 'gwei')
    }

    signed_tx = web3.eth.account.signTransaction(tx, initService.keys["private"])
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# TODO : use address variables instead of hardcoded
def fetchActualQuote():
    print(datetime.datetime.now().isoformat() + " ##### SwapService: Actualise quote #####")
    try:
        quote = requests.get("https://api.1inch.exchange/v3.0/56/quote?fromTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&toTokenAddress=0xc2e1acef50ae55661855e8dcb72adb182a3cc259&amount=10000000000000000000&").json()
        return quote
    except:
        return None


def requestSwap(fromTokenAddress, toTokenAddress, fromAmountToSwap, slippage):
    print(datetime.datetime.now().isoformat() + " ##### SwapService: Request to swap #####")
    try:
        #swapRequest = requests.get("https://api.1inch.exchange/v3.0/56/swap?fromTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&toTokenAddress=0xc2e1acef50ae55661855e8dcb72adb182a3cc259&amount=10000000000000000000&fromAddress=0xb11e4CB63F8a2c998353be3E30A00486312433aa&slippage=1").json()
        swapRequest = requests.get("https://api.1inch.exchange/v3.0/56/swap?fromTokenAddress=" + fromTokenAddress + "&toTokenAddress=" + toTokenAddress + "&amount=" + str(applyTokenDecimals(fromAmountToSwap,fromTokenAddress)) + "&fromAddress=0xb11e4CB63F8a2c998353be3E30A00486312433aa&slippage=" + str(slippage)).json()
        print(swapRequest)
        return swapRequest
    except:
        print("https://api.1inch.exchange/v3.0/56/swap?fromTokenAddress=" + fromTokenAddress + "&toTokenAddress=" + toTokenAddress + "&amount=" + str(applyTokenDecimals(fromAmountToSwap,fromTokenAddress)) + "&fromAddress=0xb11e4CB63F8a2c998353be3E30A00486312433aa&slippage=" + str(slippage))
        print(datetime.datetime.now().isoformat() + " ##### SwapService: Swap failed #####")

def signTx(tx):
    print(datetime.datetime.now().isoformat() + " ##### SwapService: Sign tx #####")
    nonce = { "nonce" : web3.eth.getTransactionCount(initService.keys["public"]) }
    tx.update(nonce)
    print(tx)
    tx["value"]=int(tx["value"])
    tx["gasPrice"] = int(tx["gasPrice"])
    tx["to"] = web3.toChecksumAddress(tx["to"])
    return web3.eth.account.signTransaction(tx, initService.keys["private"])

def sendTx(signed_tx):
    print(datetime.datetime.now().isoformat() + " ##### SwapService: Send tx #####")
    return web3.eth.sendRawTransaction(signed_tx.rawTransaction)


def applyTokenDecimals(amount, tokenAddress):
    decimals = tokenService.getDecimals(tokenAddress)
    return amount * pow(10,decimals)




