import threading, os

def task1():
    print('task 1 assigned to thread: {}'.format(threading.current_thread().name))
    print('ID of process running task 1: {}'.format(os.getpid()))

def task2():
    print('task 2 assigned to thread: {}'.format(threading.current_thread().name))
    print('ID of process running task 2: {}'.format(os.getpid()))

if __name__ == '__main__':

    # create threads
    t1=threading.Thread(target=task1, name='t1')
    t2=threading.Thread(target=task2, name='t2')

    # start threads
    t1.start()
    t2.start()

    # wait until threads are completed
    t1.join()
    t2.join()

    # both threads are finished
    print("Done!")
