from multiprocessing import Lock, Condition, Value

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


class CheatMonitor:
    def __init__(self):
        self.mutex = Lock()
        self.eating = Value('i', 0)
        self.other = Condition(self.mutex)
    
    def is_eating(self, num:int):
        self.mutex.acquire()
        self.eating.value += 1
        self.other.notify()
        self.mutex.release()
    
    def wants_think(self, num:int):
        self.mutex.acquire()
        self.other.wait_for(lambda : self.eating.value > 1, timeout=1)
        self.eating.value -= 1
        self.mutex.release()

class AnticheatTable:
    def __init__(self, size, manager):
        self.mutex = Lock()
        self.size = size
        self.manager = manager
        self.philosophers = self.manager.list([False]*size)
        self.hungry = self.manager.list([False]*size)
        self.freefork = Condition(self.mutex)
        self.chungry = Condition(self.mutex)
    
    def set_current_phil(self, num:int):
        self.current_phil = num
    
    def can_eat(self):
        num = self.current_phil
        return not self.philosophers[(num-1)%self.size] and not self.philosophers[(num+1)%self.size]
    
    def not_hungry(self):
        num = self.current_phil
        return not self.hungry[(num+1)%self.size]
    
    def wants_eat(self, num:int):
        self.mutex.acquire()
        #print(f"Philosopher {num} waiting for hungry {(num+1)%self.size}")
        self.hungry[num] = True
        
        self.chungry.wait_for(self.not_hungry)
        
        print(f"Philosopher {num} hungry")
        self.freefork.wait_for(self.can_eat)
        self.philosophers[num] = True
        self.hungry[num] = False
        self.chungry.notify_all()
        self.mutex.release()
    
    def wants_think(self, num:int):
        self.mutex.acquire()
        self.philosophers[num] = False
        self.freefork.notify_all()
        self.mutex.release()
    