import unittest
from unittest.mock import patch
from services.TradingPairService import FetchTradingPairs
from services.TradingPairService import fetchTradingPairSetting

class TestTradingPairs(unittest.TestCase):
    def test_fetch_trading_pairs(self):
        """
        Test that a list of tradingpairs can be read from JSON file via FetchTradingPairs()
        Implicitly also the ConvertToList is tested
        """
        with patch('services.TradingPairService.initService.getTradingPairsFileLocation') as mocked_trading_pairs_file_location:
            mocked_trading_pairs_file_location.return_value = "./data/tradingpairs.json"
            tradingPairList = FetchTradingPairs()
            self.assertEqual(len(tradingPairList), 1)
            self.assertEqual(tradingPairList[0].baseToken, "BUSD")
            self.assertEqual(tradingPairList[0].swapToken, "BTS")
            self.assertEqual(tradingPairList[0].moonBagPercentage, 0)
            self.assertEqual(tradingPairList[0].allocationPercentage, 10)
            self.assertEqual(tradingPairList[0].takeProfitPercentage, 1.5)
            self.assertEqual(tradingPairList[0].minimumDistance, -0.5)
            self.assertEqual(tradingPairList[0].minimumOrderSize, 10)
            self.assertEqual(tradingPairList[0].maxBuyPrice, 140)
            self.assertEqual(tradingPairList[0].pathPreferred, "PANCAKESWAP")
            self.assertEqual(tradingPairList[0].maxOutstandingBuyOrders, 10)
            self.assertEqual(tradingPairList[0].slippage, 2)
            self.assertEqual(tradingPairList[0].baseTokenAddress, "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56")
            self.assertEqual(tradingPairList[0].swapTokenAddress, "0xc2e1acef50ae55661855e8dcb72adb182a3cc259")
            self.assertEqual(tradingPairList[0].dateTimeStamp, "2021-04-02T23:27:09.277886")


    def test_fetchTradingPairSetting(self):
        """
        Test the fetchTradingPairSetting, retrieve all possible parameters
        """
        with patch('services.TradingPairService.initService.getTradingPairsFileLocation') as mocked_trading_pairs_file_location:
            mocked_trading_pairs_file_location.return_value = "./data/tradingpairs.json"
            parameter = fetchTradingPairSetting("BUSD", "BTS", "moonBagPercentage")
            self.assertEqual(parameter, 0)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "allocationPercentage")
            self.assertEqual(parameter, 10)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "takeProfitPercentage")
            self.assertEqual(parameter, 1.5)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "minimumDistance")
            self.assertEqual(parameter, -0.5)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "minimumOrderSize")
            self.assertEqual(parameter, 10)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "maxBuyPrice")
            self.assertEqual(parameter, 140)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "pathPreferred")
            self.assertEqual(parameter, "PANCAKESWAP")
            parameter = fetchTradingPairSetting("BUSD", "BTS", "maxOutstandingBuyOrders")
            self.assertEqual(parameter, 10)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "slippage")
            self.assertEqual(parameter, 2)
            parameter = fetchTradingPairSetting("BUSD", "BTS", "baseTokenAddress")
            self.assertEqual(parameter, "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56")
            parameter = fetchTradingPairSetting("BUSD", "BTS", "swapTokenAddress")
            self.assertEqual(parameter, "0xc2e1acef50ae55661855e8dcb72adb182a3cc259")


if __name__ == '__main__':
    unittest.main()