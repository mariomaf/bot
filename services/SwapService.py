import entity.swap
import requests, datetime
import services.SellOrderService as sellOrderService
import services.InitService as initService
from web3 import Web3

def swapBuyOrder(buyOrder, quoteResponse):
    # 1. Prepare Swap
    slippage = 2
    swapOrder = entity.swap.Swap(buyOrder.baseToken,
                            buyOrder.swapToken,
                            quoteResponse.toAmount,
                            buyOrder.amount,
                            buyOrder.amount/quoteResponse.toAmount,
                            "BUY",
                            slippage,
                            buyOrder,
                            quoteResponse)
    print("test", swapOrder.toJSON())
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
    print("test", swapOrder.toJSON())
    executeSwap(swapOrder)


# NOT USED YES
def executeSwap(swapOrder):
    # execute health check of exchange API
    if requests.get('https://api.1inch.exchange/v3.0/56/healthcheck').json()["status"] == "OK":
        print(datetime.datetime.now().isoformat() + " ##### SwapService: Exchange health check okey #####")
        # TODO: 2. Check if approved
        # 3. Execute Swap
        # TODO: BB-8 not implemented yet
        # 4. Creat SellOrder
        # TODO: make this part of the return as in:
        # return sellOrderService.placeVirtualSellOrder(swapOrder)
        if swapOrder.type == "BUY":
            sellOrderService.placeVirtualSellOrder(swapOrder)
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









