from multiprocessing import Process, Condition, Semaphore, Lock, Array, Manager, Value
import time
from random import random

from monitor import AnticheatTable, CheatMonitor

NPHIL = 5
K = 10


def delay(n):
    time.sleep(random()/n)

def philosopher_task(num:int, table:AnticheatTable, cheat:CheatMonitor):
    table.set_current_phil(num)
    k = 0
    while k < K:
        print(f"Philosopher {num} thinking {k}")
        print(f"Philosopher {num} wants to eat {k}")
        table.wants_eat(num)
        if num == 0 or num == 2:
            cheat.is_eating(num)
        print(f"Philosopher {num} eating {k}")
        if num == 0 or num == 2:
            cheat.wants_think(num)
        table.wants_think(num)
        print(f"Philosopher {num} stops eating {k}")
        k += 1

def main():
    manager = Manager()
    table = AnticheatTable(NPHIL, manager)
    cheat = CheatMonitor()
    philosophers = [Process(target=philosopher_task, args=(i,table, cheat)) \
                    for i in range(NPHIL)]
    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()

if __name__ == '__main__':
    main()
    
