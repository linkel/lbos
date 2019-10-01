# Let's say we have two threads and they are using the shared variable count.

import threading

count = 0

def fun1():
    global count
    while count < 10:
        print(count)
        count += 1

def fun2():
    global count
    while count < 10:
        print(count)
        count += 1

t = threading.Thread(target = fun1)
t2 = threading.Thread(target = fun2)

t.start()
t2.start()

print(count)

# hilarious! On first run, I get a glorious
# 0,0,1,1,3,2,5,4,6,8,9,7

# Let's say we don't want this to happen! 
# How can I keep the threads from willynillying incrementing?

print("okay, let's try this again with a mutual exclusion!")
count = 0

mutex = threading.Semaphore(1)

def fun3():
    global count
    while count < 10:
        mutex.acquire()
        print(count)
        count += 1
        mutex.release()

def fun4():
    global count
    while count < 10:
        mutex.acquire()
        print(count)
        count += 1
        mutex.release()

t = threading.Thread(target = fun3)
t2 = threading.Thread(target = fun3)

t.start()
t2.start()

print(count)


# It looks like because I chose to go with while loops to show the effect harder,
# unlike the book which uses a single count increment, there's something else going on.
# The mutex'd code definitely prints in order but sometimes has duplicate numbers printed out.
# the non mutex'd code is all over the place, which is expected.

# Very cool!

# i can probably also combine the functions since they are SYMMETRICAL--code is not different between threads.
