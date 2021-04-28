import unittest
from unittest.mock import patch
from services.SellOrderService import fetchSellOrders

class TestSellOrders(unittest.TestCase):
    def test_fetch_sell_order_list(self):
        """
        Test that a list of virtual sell orders can be read from JSON file via fetchSellOrderList()
        Implicitly also the ConvertToList is tested
        """
        with patch('services.SellOrderService.InitService.getSellOrdersFileLocation') as mocked_sell_orders_file_location:
            mocked_sell_orders_file_location.return_value = "./data/sellorders.json"
            sellOrderList = fetchSellOrders()
            # first assert the sell order itself
            self.assertEqual(len(sellOrderList), 2)
            self.assertEqual(sellOrderList[0].baseToken, "BTS")
            self.assertEqual(sellOrderList[0].swapToken, "BUSD")
            self.assertEqual(sellOrderList[0].buyprice, "116.35042")
            self.assertEqual(sellOrderList[0].sellprice, 118.0956763)
            self.assertEqual(sellOrderList[0].amount, "0.08595")
            self.assertEqual(sellOrderList[0].amountSwapped, 10.150323377984998)
            self.assertEqual(sellOrderList[0].expectedprofit, 0.1500047789849983)
            self.assertEqual(sellOrderList[0].takeprofitpercentage, 1.5)
            self.assertEqual(sellOrderList[0].UUID, "98148973-d59e-458a-bd0e-600b5222d26c")
            self.assertEqual(sellOrderList[0].dateTimeStamp, "2021-04-25T19:14:34.872256")


if __name__ == '__main__':
    unittest.main()