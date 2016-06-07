=======
Deckor
=======

Decorate your functions and with 'deckor'ators. A module created while learning decorators.

Installation
=============

    pip install deckor


Decorators Supported:
======================

* timer : Measure execution time of functions

    @deckor.timer
    def fact(x):
        if x <= 0:
            return 1
        return x*fact(x-1)

* cacheit : Cache intermediate results

    @deckor.cacheit
    def fact(x):
        if x <= 0:
            return 1
        return x*fact(x-1)

* trace : Print the pretty recursion trace

    @deckor.trace
    def fib(x):
        if x < 2:
            return x
        return fib(x-1)+fib(x-2)

    fib(10)

    Now, try trace with cacheit

    @deckor.cacheit
    @deckor.trace
    def fib(x):
        if x < 2:
            return x
        return fib(x-1)+fib(x-2)

    fib(10)

* with_retries : function signature: with_retries(tries=5, delay=0, increment=0). Try execution of function with retries. Retry'tries' no of times. Delay of 'delay' seconds between retries. Increase the delay by 'increment' between retries

    @with_retries(5)
    def random_f():
        try: r = requests.get("random")
        except: return

* syncronize : Provides very basic syncronization. Note: Not free from race condition only for basic usage

    import threading
    
    lock = threading.Lock()
    sample_list = []

    @deckor.syncronize(lock)
    def sample(sample_list):
        sample_list.append(1)

    #sample list is modified only after lock is acquired
    #so, mdification is sample_list os thread safe


