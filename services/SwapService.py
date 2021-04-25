import entity.swap
import services.TradingPairService as tradingPairService


def swapBuyOrder(buyOrder, quoteResponse):
    # 1. Prepare Swap
    slippage = 2
    swap = entity.swap.Swap(buyOrder.baseToken,
                            buyOrder.swapToken,
                            quoteResponse.toAmount,
                            buyOrder.amount,
                            buyOrder.amount/quoteResponse.toAmount,
                            "BUY",
                            slippage)
    print("test", swap.toJSON())
    # 2. Execute Swap


    # 3. Create Sell Order based on Swap




