'''
multiprocessing.Queue
'''

# import time
# from multiprocessing import Process, Queue

# def f(q0, q1, n):
#     for i in range(n):
#         q0.put(0)
#         q1.get()

# def main():
#     pass

# if __name__ == '__main__':
#     n = 20000
#     q0, q1 = Queue(), Queue()
#     p = Process(target=f, args=(q0, q1, n))
#     p.start()

#     t0 = time.time()
#     for i in range(n):
#         q0.get()
#         q1.put(0)
#     print 'Queue latency: {} ms'.format((time.time() - t0) / (n*2) * 1E6)
#     p.join()


# import time
# from multiprocessing import Process, Pipe

# def f(q1, n):
#     for i in range(n):
#         q1.send(0)
#         q1.recv()

# if __name__ == '__main__':
#     n = 10000
#     q0, q1 = Pipe()
#     p = Process(target=f, args=(q1, n))
#     p.start()

#     t0 = time.time()
#     for i in range(n):
#         q0.recv()
#         q0.send(0)
#     print 'Pipe latency: {} ms'.format((time.time() - t0) / (n*2) * 1E6)
#     p.join()



# import time
# from multiprocessing import Process, Array

# def f(a, n):
#     for i in range(n):
#         a[0] = i + 1
#         while a[1] == i:
#             pass

# if __name__ == '__main__':
#     n = 100000
#     a = Array('i', [0,0])
#     p = Process(target=f, args=(a, n))
#     p.start()

#     t0 = time.time()
#     for i in range(n):
#         while a[0] == i:
#             pass
#         a[1] = i + 1
#     print 'Shared Array latency: {} ms'.format((time.time() - t0) / (n*2) * 1E6)
#     p.join()

import time
from multiprocessing import Process, Array

def f(a, n):
    for i in range(n):
        a[0] = i + 1
        while a[1] == i:
            pass

if __name__ == '__main__':
    n = 10000
    a = Array('i', [0,0], lock=False)
    p = Process(target=f, args=(a, n))
    p.start()

    t0 = time.time()
    for i in range(n):
        while a[0] == i:
            pass
        a[1] = i + 1
    print('Array latency: ', (time.time() - t0) / (n*2) * 1E6, 'microseconds')

    p.join()