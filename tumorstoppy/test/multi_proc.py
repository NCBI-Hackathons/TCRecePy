from multiprocessing import Process
import os
from time import time

def f():
    return 1

m = 0;

t1 = time()
for i in range(10000):
    m += pool.apply_async(f,()).get(timeout=1)
t2 = time()
print (t2-t1)

t3 = time()
for i in range(10000):
    m += f()
t4 = time()
print(t4-t3)

