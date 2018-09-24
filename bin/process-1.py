import logging
import threading
import time
from multiprocessing import Process

class Data(object):
    def __init__(self):
        self.storage = 0
        self.test = 999
    def set(self, value):
        self.storage = value
    def get(self):
        return self.storage

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def _counter(maxvalue=99999):
    value = 0
    yield value
    while True:
        value += 1
        if maxvalue != -1 and value > maxvalue - 1:
            value = 0
        yield value

def reader():
    start_time = time.time()
    while time.time() - start_time < 5:
        print data.test

if __name__ == '__main__':
    logger = get_logger()
    data = Data()
    # thread_names = ['Mike', 'George', 'Wanda', 'Dingbat', 'Nina']
    # for i in range(5):
    #     my_thread = threading.Thread(
    #         target=square, name=thread_names[i], args=(i,logger))
    #     my_thread.start()
    counter = _counter(10)

    proc = Process(target=reader)
    proc.start()
    # proc.join()

    start_time = time.time()
    while time.time() - start_time < 5:
        data.test +=1
        data.set(counter.next())
        print data.get()


