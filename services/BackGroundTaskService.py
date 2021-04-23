import entity.backGroundTasks

def startBackGroundTasks():
    q = entity.backGroundTasks.QuoteScheduler()
    q.start()



    t = entity.backGroundTasks.BuyOrderScheduler()
    t.start()

def restartEngine():
    print('trying to stop engine')
    # TODO
