## Rendezvous

Cool thing about rendezvous! I wrote some code in the runnable rendezvous.py file like:

```
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
```

So you could also write the functions something like this:

```
def fun_a():
    print("my a1 statement")
    a1_done.release()
    b1_done.acquire()
    print("my a2 statement")

def fun_b():
    print("my b1 statement")
    a1_done.acquire()
    b1_done.release()
    print("my b2 statement")
```

Would still work. In fact, that's how I wrote it in response to the puzzle posed in the book at first. But interestingly this way may cause one more thread switchover than the other one.

Only if b runs first, though.

```
                   a a  b b
                   4 2  1 3
a1                   |  |    b1
a1_done.release()    |  |    a1_done.acquire()
b1_done.acquire()  | |    |  b1_done.release()
a2                 |      |  b2
```

If a runs first then it performs the same as if we did both releases then acquires for both threads.

```
                   a a b
                   1 3 2
a1                 |   |    b1
a1_done.release()  |   |    a1_done.acquire()
b1_done.acquire()  |   |    b1_done.release()
a2                   | |    b2
```