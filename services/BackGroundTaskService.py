import entity.backGroundTasks

def startBackGroundTasks():
    q = entity.backGroundTasks.QuoteScheduler()
    q.start()

    t = entity.backGroundTasks.BuyOrderScheduler()
    t.start()

