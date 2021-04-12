import threading
import time
import services.QuoteService as quoteService
import services.BuyOrderService as buyOrderService
import services.InitService as initService

class QuoteScheduler(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            quoteService.ScheduledQuoteRequest()
            time.sleep(initService.getQuoteInterval())

class BuyOrderScheduler(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            buyOrderService.placeVirtualBuyorders()
            time.sleep(initService.getBuyOrderInterval())