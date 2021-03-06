import functools
import time

def lru_cache(max_size):
    cache: dict = {}
    hits = misses = 0

    def deco(user_func):
        @functools.wraps(user_func)
        def inner(*arg_func, **kwargs):
            result = user_func(*arg_func, **kwargs)
            key = arg_func + tuple(sorted(kwargs.items()))
            nonlocal cache, misses, hits
            if cache.get(key):
                hits += 1
                cache[key]['time'] = time.time()
            else:
                if len(cache) < max_size:
                    cache[key] = {'result': result, 'time': time.time()}
                    misses += 1
                elif len(cache) >= max_size:
                    dict_for_max = {}
                    for item in cache:
                        dict_for_max[item] = cache.get(item).get('time')
                    del_key = max([key_for_del for key_for_del, value_for_del in dict_for_max.items() if
                                   value_for_del == max(dict_for_max.values())])
                    del cache[del_key]
                    cache[key] = {'result': result, 'time': time.time()}
                    misses += 1
            
            return cache[key]['result']

        def info():
            nonlocal hits, misses, cache, max_size
            return 'hits: {}, misses: {}, size: {}, max_size: {}'.format(hits, misses, len(cache), max_size)

        def clear():
            nonlocal hits, misses
            cache.clear()
            hits = 0
            misses = 0

        inner.clear = clear
        inner.info = info
        inner.cache = cache
        return inner

    return deco


@lru_cache(max_size=6)
def fib(n) -> int:
    """
    the Fibonacci Sequence
    """
    if n < 2:
        time.sleep(0.005)
        return n
    return fib(n - 1) + fib(n - 2)


fib(10)
print(fib.info())
print(fib.cache)
