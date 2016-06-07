
import time
from functools import wraps


def timer(f):
    """Profile your functions.
    Prints the time taken by a function"""

    @wraps(f)
    def _timer(*args, **kwargs):
        start = time.time()
        rsp = f(*args, **kwargs)
        timer = time.time() - start
        print("Time: %fs" % (timer))
        return rsp

    return _timer


def cacheit(f):
    """cache the intermediate result of the calculation.
    Uses the passwed argument join string as key"""

    cache_dict = {}
    @wraps(f)
    def _cacheit(*args, **kwargs):
        if args:
            key = ''.join(map(str, args))
            if kwargs:
                key += ''.join(map(str, d.items()))
            if cache_dict.get(key):
                return cache_dict[key]
            else:
                cache_dict[key] = f(*args, **kwargs)
            return cache_dict[key]
        else:
            return f(*args, **kwargs)

    return _cacheit


def trace(f):
    """Print pretty trace of function calls"""
    #python2 outer scope limitation
    level = [0]
    def _log(text):
        indent = '|    ' * level[0] + '|--> '
        print(indent + text)

    @wraps(f)
    def _trace(*args, **kwargs):
        #global level
        argstr = '(' + ", ".join([repr(a) for a in args]) + ")"
        _log(f.__name__ + argstr)

        level[0] += 1
        ret = f(*args, **kwargs)
        _log("return " + repr(ret))
        level[0] -= 1
        return ret

    return _trace


def with_retries(tries, delay=0, increment=0):
    """Try execution of function with retries. Retry'tries'
    no of times. Delay of 'delay' seconds between retries.
    Increase the delay by 'increment' between retries"""

    if not isinstance(tries, int) or tries < 0:
        raise ValueError("tries must be a positive integer.")

    if not isinstance(delay, int) or delay < 0:
        raise ValueError("delay must be a positive integer.")

    if not isinstance(increment, int) or increment < 0:
        raise ValueError("increment must be a positive integer.")

    def retry(f):
        _tries = [tries]
        _delay = [delay]
        def _retry(*args, **kwargs):
            ret = None
            while(_tries[0] > 0):
                print("Retry: {}".format(tries - _tries[0] + 1))
                try:
                    ret = f(*args, **kwargs)
                    if ret != None:
                        return ret
                except Exception as e: pass
                
                time.sleep(_delay[0])
                _delay[0] += increment
                _tries[0] -= 1
        return _retry
    return retry


def syncronize(lock):
    """Syncronize two or more functions"""

    def locker(f):
        def _locker(*args, **kwargs):
            lock.acquire()
            try:
                ret = f(*args, **kwargs)
                return ret
            except Exception as e:
                raise Exception(e)
            finally:
                lock.release()
        return _locker
    return locker


"""
def func_counter(f):
    Prints the count of number of times
    function is called

    @wraps(f)
    def count_inc(*args, **kwargs):
        if count_inc.counter == 0:
            count_inc.counter = 0

        count_inc.counter += 1
        ret = f(*args, **kwargs)
        print("Count: {}".format(count_inc.counter))
        return ret

    count_inc.counter = 0
    return count_inc
"""
