## Synchronization

Synchronization refers to relationships among events. Before, during, and after, and any number of events. 

Synchronization constraints are requirements that have to do with the order of events. 

Serialization is where Event A must happen before Event B. 

Mutual Exclusion is where A and B must not happen at the same time. MUTEX. 

How do we know if A happened before B in software? 

## Execution Model

If instructions are just one after the other, then if A comes before B, A gets executed first. 

What if the computer is parallel? Then it's running stuff on multiple processors and we don't know if a statement on one processor got executed before a statement on another. 

What if one processor is running multiple threads of execution? A thread is a sequence of instructions that execute sequentially. If there's multiple threads, then the processor can work on one, then switch to another. 

The OS's scheduler makes these decisions. No difference re: synchronization between the parallel model and the multithread model. 

## Serialization with messages

How can A make sure B doesn't eat lunch until after A's eaten lunch? A could tell B to wait for a phone call before eating lunch. 

A:
```
Eat breakfast
Work
Eat lunch
Call B
```

B:
```
Eat breakfast
Wait for a call
Eat lunch
```

So breakfast was concurrent since we don't know who ate it first, but lunch happened sequentially for sure. 

```
a1 < a2 < a3 < a4
b1 < b2 < b3
```
```
a3 < b3 
a4 < b2
```
```
a3 < a4 < b2 < b3
```

So A definitely had lunch before B. 

Two events are concurrent if we cannot tell by looking at the program which will happen first. 

## Non-determinism

Concurrent programs are often non-deterministic. 

Thread A
```
print "yes"
```

Thread B
```
print "no"
```

The order of execution just depends on the scheduler. So non-determinism makes concurrent programs hard to debug. One must program carefully. 

## Shared Variables

Sometimes variables are shared between two or more threads! If we want a thread to read a value written by another thread and they're unsynchronized, how the heck do we know if the reader will see the value that the writer wrote, or whether the reader is just going to see an old value sitting in that variable? You must constrain it so that the reader doesn't read until after the writer writes. 

Concurrent writes (two or more writers) and concurrent updates (two or more threads performing a read followed by a write) are other ways that threads can interact via a shared variable. Usually concurrent reads aren't a problem. 

## Concurrent Writes

Thread A
```
x = 5
print x
```

Thread B
```
x = 7
```

What value gets printed? 

What path yields output 5 and final value 5? If B executes first then A, then we can get that. 
What path yields output 7 and final value 7? If Thread A's step 1 executes, then Thread B executes, and thread A's step 2 executes, then we will have output 7 and final value 7. 
Is there a path that yields output 7 and final value 5? 

I don't think there can be one. That would require B to have happened, and then step 2 of A to happen before step 1. In Thread A, which will execute in order, it's step 1 < step 2, and B is just step 1 of B. There's no way to stick B in anywhere in this sequence to get an output 7 and final value 5. But we can totally get output 5 and final value 7, if we get a x = 5 print x x = 7.

But does that count as a proof? Curious to see what passes as a proof here. 

## Concurrent Updates

An update is an operation that reads the value of a variable, computes a new value based on the old onem then writes the new one. 

Most commonly, this is an increment. New value will be the old value plus one. 

Thread A
```
count = count + 1
```

Thread B
```
count = count + 1
```

When these operations get translated into machine language, this is really a read and a write, not just ONE operation. 

Thread A
```
temp = count
count = temp + 1
```

Thread B
```
temp = count 
count = temp + 1
```

So if we consider the execution path of a1 < b1 < b2 < a2 , if the initial value of x is 0, what's the final value? 

Final value will be 1. Variable only got incremented 1x. 

Downey says that this kind of problem is subtle because it's not always possible to tell which operations are performed in one step and which can be interrupted. 

Some computers actually have increment instructions that are hardware-implemented and can't be interrupted. If an op can't be interrupted, it is said to be ATOMIC. 

How can we write concurrent programs if we don't know which operations are atomic? You could collect specific information about each operation on each hardware platform but this is overwhelming and very specific. You could also make an assumption that all updates and all writes are not atomic, and then use synchronization constraints to control concurrent access to shared variables. 

So then the most common constraint here is mutex. This is mutual exclusion--this guarantees that only one thread accesses a shared variable at a time. 

Suppose that 100 threads run the following program concurrently. 

```
for i in range(100):
temp = count
count = temp + 1
```
What is the largest possible value of count after all threads have completed?

What is the smallest possible value? 

I am assuming count begins at 0.
Okay, so if it so happened that all 100 threads ran in this perfect order then the largest value would be 10000.

Is it possible for all the threads to grab the count and then end up just incrementing once? Does running happen between in the for loop too for each thread? Like can they all just keep grabbing the exact same number each loop and just end up at 100? 

## Mutual Exclusion with messages

We can implement mutual exclusion with message passing, just like with serialization. 
