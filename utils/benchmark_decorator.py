

import time
from transit.network import Network
import functools


def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        network = args[0]
        start = args[1]
        end = args[2]

        start_time=time.perf_counter()
        result=func(*args,**kwargs)
        end_time=time.perf_counter()
        time_taken=end_time-start_time
        nodes = network.router.visited_nodes

        return {
            "time": time_taken,
            "node": nodes,
            "result": result
        }
    return wrapper
