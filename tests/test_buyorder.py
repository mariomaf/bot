import unittest
from unittest.mock import patch
from services.BuyOrderService import fetchBuyOrderList



class TestBuyOrders(unittest.TestCase):
    def test_fetch_buy_order_list(self):
        """
        Test that a list of virtual buy orders can be read from JSON file via fetchBuyOrderList()
        Implicitly also the ConvertToList is tested
        """
        with patch('services.BuyOrderService.InitService.getBuyOrderFileLocation') as mocked_buy_orders_file_location:
            mocked_buy_orders_file_location.return_value = "./data/buyorders.json"
            buyOrderList = fetchBuyOrderList()
            self.assertEqual(len(buyOrderList[0]), 1)
            self.assertEqual(len(buyOrderList[0]["BTSBUSD"]), 10)
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].baseToken, "BUSD")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].swapToken, "BTS")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].buyprice, "129.90138")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].amount, 10)
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].amountSwapped, "0.07698")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].lastpricequote, "130.56071")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].distancepercentage, "99.5")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].UUID, "667e1110-c408-459e-83b8-6deb66d2e5e9")
            self.assertEqual(buyOrderList[0]["BTSBUSD"][0].dateTimeStamp, "2021-04-28T16:44:30.038654")





if __name__ == '__main__':
    unittest.main()
