import threading

# It's a SEMAPHORE! With an initial value of 0.
# This means that if a thread acquires/decrements/waits this dude,
# it is gonna LOCK til it gets released. 

# I will call it a1done. Because we're gonna use it to show when
# a1 has printed its message.

# Basically, I want the a1 message to print before b1!

a1done = threading.Semaphore(0)

def function_a():
    print("My a1 message")
    a1done.release()

def function_b():
    a1done.acquire()
    print("My b1 message")

# Here I'm making sure I start t2 before t1 so normally function b would print first
# You can see if you comment out the semaphore acquire, that b1 will go first

# But since I have it acquiring, it's gotta wait til a1 releases.

t2 = threading.Thread(target = function_b)
t2.start()
t = threading.Thread(target = function_a)
t.start()