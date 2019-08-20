import multiprocessing

def job(q):
    res = 0
    for i in range(10):
        res += i
    q.put(res)


if __name__ == "__main__":
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=job, args=(q,))
    p2 = multiprocessing.Process(target=job, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    res1 = q.get()
    res2 = q.get()
    print("res:", res1 + res2)


