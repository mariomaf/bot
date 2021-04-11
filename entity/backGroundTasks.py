import threading
import time
import services.QuoteService as quoteService
import services.InitService as initService

class BackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        while True:
            quoteService.ScheduledQuoteRequest()
            time.sleep(initService.getQuoteInterval())