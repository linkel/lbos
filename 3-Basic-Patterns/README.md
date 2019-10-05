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

# Barriers

Kinda cool--so the rendezvous with two threads can be generalized to more threads! Then it gets called a barrier. 

```
threads come in here!

rendezvous (make 'em all stop until they're all ready)

critical point
```

When the first n - 1 threads arrive, they block until the nth thread arrives, at which point they all go on. 

This one really tripped me up--not used to thinking about it yet. 

We have n number of threads, we have a shared variable count that starts at 0, and we're going to need a semaphore starting at 1 and a semaphore starting at 0. 

Let's say we have 4 threads. 

```
mutex.wait()
    count += 1
mutex.signal()

if count == 4:
    blocker.signal()

blocker.wait()
blocker.signal()

CRITICAL POINT

```

We need the signal on the blocker right after the wait because otherwise, only ONE thread gets through! When three threads are waiting at blocker, it's at -3. The one signal from the 4th permits one guy through but it's still at -2 and then the 4th dude comes in and now it's back at -3, with only one thread managing to make it to the critical point. DEADLOCK!

So yep, needs signal right after the wait. Apparently a very common pattern. Called a Turnstile! 

# Reusable Barrier

Now let's say the code's looping. And we want to keep the barrier going, so every time all four threads need to be at the barrier before it opens up, then it will loop back to the top. 

This one's a doozy (for me). And the book's author predicted my initial attempt at a solution, where we decrement count back down to 0 in a mutex. 

It felt like he was reading my mind when I scrolled down to "non-solution #1 and #2". 

Here's a NON SOLUTION!

```
mutex.wait()
    count += 1
mutex.signal()

if count == n: barrier.signal()

barrier.wait()
barrier.signal()

CRIT POINT

mutex.wait()
    count -= 1
mutex.signal()

if count == 0: barrier.wait()
```

The above one is no good because of thread interruption. If thread gets interrupted at line 7 and then both threads read a count == n then they both signal the turnstile and now everything gets through forever. 

The other non solution:

```
mutex.wait()
    count += 1
    if count == n: barrier.signal()
mutex.signal()

barrier.wait()
barrier.signal()

CRIT POINT

mutex.wait()
    count -= 1
    if count == 0: barrier.wait()
mutex.signal()
```

You can't just have one barrier and the decrement count in mutex because if one thread just KEPT running it could end up lapping the other ones. Like imagine one thread making it through when count hits 4 in our previous example--he goes ahead and reduces the count, and it says if count is 0 barrier.wait but count ain't 0 yet so the thread loops, and breezes past barrier.wait() since barrier's at (1) after all the signaling initially. 

Trick is to have TWO BARRIERS. 


