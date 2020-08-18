# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:33:05 2020

@author: Austin
"""


import time
import numpy as np

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return(fibonacci(n-1) + fibonacci(n-2))
    
def main():
    num = np.random.randint(1,25)
    #random int 1 to 25
    print("%dth fibonacci number is : %d"%(num, fibonacci(num)))

starttime = time.time()
timeout = time.time() + 60*2
while time.time() <= timeout:
    try:
        main()
        time.sleep(5 - ((time.time() - starttime)% 5.0))
        #5s interval between each new execution
    except KeyboardInterrupt:
        print("keyboard exception recieved. ending")
        exit()
        