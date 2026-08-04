
from typing import Callable, Any
import time
from transit.network import Network
import functools


def benchmark(func: Callable[..., Any]) -> Callable[..., dict[str, Any]]:
    @functools.wraps(func)
    def wrapper(*args: Any , **kwargs: Any ) -> dict[str, Any]:
        network: Network = args[0]
        start: str = args[1]
        end: str = args[2]

        start_time: float =time.perf_counter()
        result: Any =func(*args,**kwargs)
        end_time: float =time.perf_counter()
        time_taken: float =end_time-start_time
        nodes: int = network.router.visited_nodes

        return {
            "time": time_taken,
            "node": nodes,
            "result": result
        }
    return wrapper
