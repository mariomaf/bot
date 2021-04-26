import entity.swap
import services.SellOrderService as sellOrderService

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
    # 2. Execute Swap
    # TODO: BB-8 not implemented yet
    # 3. Creat SellOrder
    # TODO: make this part of the return as in:
    # return sellOrderService.placeVirtualSellOrder(swapOrder)
    if swapOrder.type == "BUY":
        sellOrderService.placeVirtualSellOrder(swapOrder)
    elif swapOrder.type == "SELL":
        print("test temp")
    return










