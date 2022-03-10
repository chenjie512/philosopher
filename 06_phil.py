from multiprocessing import Process, Condition, Lock, Array, Manager
import time
from random import random

from monitor import Table

NPHIL = 5
K = 10


def delay(n):
    time.sleep(random()/n)

def philosopher_task(num:int, table:Table):
    table.set_current_phil(num)
    k = 0
    while k < K:
        print(f"Philosopher {num} thinking")
        print(f"Philosopher {num} wants to eat")
        table.wants_eat(num)
        print(f"Philosopher {num} eating")
        table.wants_think(num)
        print(f"Philosopher {num} stops eating")
        k += 1

def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    philosophers = [Process(target=philosopher_task, args=(i,table)) \
                    for i in range(NPHIL)]
    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()

if __name__ == '__main__':
    main()
    
