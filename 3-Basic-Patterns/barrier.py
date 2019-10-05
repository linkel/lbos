# Notice how without the barrier the threads all just get to print WE MADE IT,
# but with the barrier they've gotta stay together.

import threading

mutex = threading.Semaphore(1)
barrier = threading.Semaphore(0)

no_barrier_count = 0
count = 0

def without_barrier():
    global no_barrier_count
    mutex.acquire()
    no_barrier_count += 1
    print(no_barrier_count)
    mutex.release()

    print("WE MADE IT!")

def with_barrier():
    global count
    mutex.acquire()
    count += 1
    print(count)
    mutex.release()

    if count == 4:
        barrier.release()
    
    barrier.acquire()
    barrier.release()

    print("WE MADE IT!")


threading.Thread(target=without_barrier).start()
threading.Thread(target=without_barrier).start()
threading.Thread(target=without_barrier).start()
threading.Thread(target=without_barrier).start()

threading.Thread(target=with_barrier).start()
threading.Thread(target=with_barrier).start()
threading.Thread(target=with_barrier).start()
threading.Thread(target=with_barrier).start()
