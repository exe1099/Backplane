from multiprocessing import Process, Queue
import time
import sys

def reader(queue):
    ## Read from the queue; this will be spawned as a separate Process
    while True:
        msg = queue.get()         # Read from the queue and do nothing
        print(msg)
        if (msg == 'DONE'):
            break

def writer_proc(queue):
    ## Write to the queue
    i = 0
    while True:
        queue.put(i)             # Write 'count' numbers into the queue
        time.sleep(2)
        i += 1

if __name__=='__main__':
    queue = Queue() # writer() writes to pqueue from _this_ process
    ### reader_proc() reads from pqueue as a separate process
    writer_p = Process(target=writer_proc, args=((queue),))
    writer_p.daemon = True
    writer_p.start()        # Launch reader_proc() as a separate python process

    while True:
        if queue.empty():
            print("Empty queue!")
        else:
            print(queue.get())
        time.sleep(0.5)
