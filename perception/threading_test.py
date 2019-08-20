import threading
import time

# def thread_job():
#     print("aaaaa")
#     print(threading.current_thread())
#     for i in range(10):
#         time.sleep(0.1)
#     print("T1 done")

# def thread2_job():
#     print("bbbb")
#     print(threading.current_thread())
#     for i in range(10):
#         time.sleep(0.1)
#     print("T2 done")

# def main():
#     t1 = threading.Thread(target=thread_job)
#     t2 = threading.Thread(target=thread2_job)
#     print(threading.active_count())
#     print(threading.enumerate())
#     print(threading.current_thread())
#     t1.start()
#     t2.start()
#     print("all done")

# def job(l, q):
#     for i in range(len(l)):
#         l[i] = l[i]**2
#     q.put(l)

# from queue import Queue
# def multithreading(data):
#     q = Queue()
#     thraeds = []
#     for i in range(4):
#         t = threading.Thread(target = job, args=(data[i], q))
#         t.start()
#         thraeds.append(t)
#     for thraed in thraeds:
#         thraed.join()
#     results = []
#     for _ in range(4):
#         results.append(q.get())
#     print(results)

# if __name__ == "__main__":
#     # main()
#     data = [[1,2,3], [3,4,5,6], [1,4,6],[2]]
#     multithreading(data)



def t1_job():
    global a, lock
    lock.acquire()
    for i in range(10):
        a += 1
        print("t1", a)
    lock.release()

def t2_job():
    global a, lock
    lock.acquire()
    for i in range(10):
        a += 1
        print("t2", a)
    lock.release()


if __name__ == "__main__":
    a = 0
    lock = threading.Lock()
    
    t1 = threading.Thread(target=t1_job)
    t2 = threading.Thread(target=t2_job)

    t1.start()
    t2.start()



