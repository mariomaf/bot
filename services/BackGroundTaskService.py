import entity.backGroundTasks

def startBackGroundTasks():
    q = entity.backGroundTasks.QuoteScheduler()
    q.start()

    # TODO: Implement a background task that actualises the sell orders based on transaction processed on the chain instead of estimated buy swapped amount

    t = entity.backGroundTasks.BuyOrderScheduler()
    t.start()

def restartEngine():
    print('trying to stop engine')
    # TODO: implement restart of engine (relevant once settings are changed via the front end
