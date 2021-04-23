import threading
import time, datetime
import services.QuoteService as quoteService
import services.BuyOrderService as buyOrderService
import services.InitService as initService


class QuoteScheduler(threading.Thread):


    def run(self,*args,**kwargs):

        while True:
            print(datetime.datetime.now().isoformat() + " ##### BackGroundTasks: Starting QuoteScheduler #####")
            quoteService.ScheduledQuoteRequest()
            print(datetime.datetime.now().isoformat() + " ##### BackGroundTasks: Finished QuoteScheduler #####")
            time.sleep(initService.getQuoteInterval())

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

class BuyOrderScheduler(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            print(datetime.datetime.now().isoformat() + " ##### BackGroundTasks: Starting BuyOrderScheduler #####")
            buyOrderService.placeVirtualBuyorders()
            print(datetime.datetime.now().isoformat() + " ##### BackGroundTasks: Finished BuyOrderScheduler #####")
            time.sleep(initService.getBuyOrderInterval())