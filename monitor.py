from multiprocessing import Lock, Condition

class Table:
    def __init__(self, size, manager):
        self.mutex = Lock()
        self.size = size
        self.manager = manager
        self.philosophers = self.manager.list([False]*size)
        self.freefork = Condition(self.mutex)
    
    def set_current_phil(self, num:int):
        self.current_phil = num
    
    def can_eat(self):
        num = self.current_phil
        return not self.philosophers[(num-1)%self.size] and not self.philosophers[(num+1)%self.size]
    
    def wants_eat(self, num:int):
        self.mutex.acquire()
        self.freefork.wait_for(self.can_eat)
        self.philosophers[num] = True
        self.mutex.release()
    
    def wants_think(self, num:int):
        self.mutex.acquire()
        self.philosophers[num] = False
        self.freefork.notify_all()
        self.mutex.release()


