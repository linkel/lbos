# Let's generalize a mutex so that multiple threads can run in the critical section at the same time.
# But we set an upper limit on the number of concurrent rheads. 

import threading

multiplex = threading.Semaphore(3)
# 3 threads, we do 3 for the semaphore!

count = 0

def fun1():
    global count
    multiplex.acquire()
    count += 1
    print(count)
    multiplex.release()

threading.Thread(target=fun1).start()
threading.Thread(target=fun1).start()
threading.Thread(target=fun1).start()

# well, due to the way it's set up in Python it works anyways without the multiplex
# but if we did have threads coming in and the scheduler picking whatever to run,
# that multiplex would help! 

# Now that we set the number in the semaphore to the number of threads,
# this means that it'll only allow 3 concurrent ones inside the critical point, since
# more than 3 would get locked.

