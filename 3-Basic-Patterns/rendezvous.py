# Hey, what if we want to generalize the signal pattern to work both ways?

# Given the code where Thread A runs
# Statement a1 
# Statement a2

# And Thread B runs 
# Statement b1
# statement b2

# We want to make a1 < b2 and b1 < a2. 

# Basically, make these guys rendezvous before they keep going.
# Neither gets to proceed until both have arrived!

import threading

a1_done = threading.Semaphore(0)
b1_done = threading.Semaphore(0)

def fun_a():
    print("my a1 statement")
    a1_done.release()
    b1_done.acquire()
    print("my a2 statement")

def fun_b():
    print("my b1 statement")
    b1_done.release()
    a1_done.acquire()
    print("my b2 statement")

t = threading.Thread(target = fun_a)
t2 = threading.Thread(target = fun_b)

t.start()
t2.start()

# You can see that if we release (or signal) our one and acquire (or wait) for the other,
# this does the rendezvous.