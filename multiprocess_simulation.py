import sys
import os
import random
import threading
from time import sleep
import time
from multiprocessing import  Process,Value,Lock
##四进程带锁，利用共享内存完成进程之间数据共享
##任务是求出连续投骰子得到1~6全部点数的总次数数学期望

threads,total=4,10000000
pure_count=0

def simulate(count,lock):
    for i in range(total//threads):
        #print('Now at {},{} terms'.format(k,i))
        list = [True for j in range(6)]
        cnt = 1
        while True:
            dict = random.randint(0, 5)
            list[dict] = False
            temp = False
            for item in list:
                if item == True:
                    temp = True
                    break
            if temp == False:
                lock.acquire()
                #print('i={} ,count={}'.format(i,count.value))
                count.value += cnt
                lock.release()
                break
            cnt += 1

def start_thread(count,lock):
    process_list=[]
    for item in range(threads):
        process = Process(target=simulate,args=(count,lock))
        process_list.append(process)
        process.start()
    for process in process_list:
        process.join()

def pure_simulate():
    global pure_count
    for i in range(total):
        list = [True for j in range(6)]
        cnt = 1
        while True:
            dict = random.randint(0, 5)
            list[dict] = False
            temp = False
            for item in list:
                if item == True:
                    temp = True
                    break
            if temp == False:
                pure_count+=cnt
                break
            cnt += 1


if __name__=='__main__':

    count = Value('i', 0)
    lock = Lock()
    start=time.time()
    start_thread(count,lock)
    end=time.time()
    print('result E(X)= ',count.value/total,'  total time= ',end-start)
    '''
    start=time.time()
    pure_simulate()
    end=time.time()
    print('result E(X)= ',pure_count/total,'  total time= ',end-start)
    '''