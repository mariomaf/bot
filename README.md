# BSC Bot

## Getting started
* create file 'keys.json' and add here the public and private key as following:

        {
            "public" : "0x11111111",
            "private" : "1111111111"
        }
* Adjust the file 'config.json' to your needs:

        {
          "quote_file_location" : "quotes_received.json",
          "buy_orders_file_location" : "data_buyorders.json",
          "trading_pairs_file_location" :"tradingpairs.json",
          "sell_orders_file_location" :"data_sellorders.json",
          "closed_swaps_file_location" :"data_closedswaps.json",
          "results_file_location" : "results.json",
          "quote_interval" : 30,
          "buy_order_interval": 300,
          "quote_history_count": 50,
          "tradeExecution" : false
        }
- Adjust the file 'tradingpairs.json' to your needs, currently only one trading pair can be set up:
  
        [
            {
                "baseToken": "BUSD",
                "swapToken": "BTS",
                "moonBagPercentage": 0,
                "allocationPercentage": 10,
                "takeProfitPercentage": 3,
                "minimumDistance": -0.5,
                "minimumOrderSize" : 25,
                "maxBuyPrice" : 200,
                "pathPreferred": "PANCAKESWAP",
                "maxOutstandingBuyOrders": 1,
                "slippage": 1,
                "baseTokenAddress": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
                "swapTokenAddress": "0xc2e1acef50ae55661855e8dcb72adb182a3cc259",
                "dateTimeStamp": "2021-04-02T23:27:09.277886"
            }
        ]