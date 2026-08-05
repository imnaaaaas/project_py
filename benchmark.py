from transit.network import Network
from utils.logger import logger
from utils.benchmark_decorator import benchmark
from typing import Any


    
@benchmark
def run_dijkstra(network : Network , start: str , end: str ) ->  list[str]:
    return network.shortest_path(start, end)


@benchmark
def run_astar(network : Network , start: str , end: str ) ->  list[str]:
    return network.shortest_path_astar(start, end)




def benchmarks_for(filename: str, routes: list[tuple[str, str]]) -> None:
    network=Network(filename)
    results_dijikstra=[]
    results_astar=[]

    for start,end in routes:
        result= run_dijkstra(network, start, end)
        results_dijikstra.append(result)

        result= run_astar(network, start, end)
        results_astar.append(result)

    time_dijkstra, node_dijkstra = total_results(results_dijikstra)
    time_astar, node_astar = total_results(results_astar)


    logger.info(f"-----{filename}-----")
    logger.info(f"dijkstra: {time_dijkstra:.6f}s {node_dijkstra} nodes")
    logger.info(f"astar: {time_astar:.6f}s {node_astar} nodes")
    logger.info("")


def total_results(results: list[dict[str, Any]]) -> tuple[float, int]:

    total_time=0
    total_node=0
    for result in results:
        total_time+=result["time"]
        total_node+=result["node"]
    return total_time, total_node


benchmarks_for("network_jsons/example_network_100.json", [("S1", "S2"), ("S1", "S50"), ("S1", "S99")])
benchmarks_for("network_jsons/example_network_1000.json", [("S1", "S2"), ("S1", "S500"), ("S1", "S1024")])
benchmarks_for("network_jsons/example_network_10000.json", [("S1", "S2"), ("S1", "S5000"), ("S1", "S10000")])



"""def benchmarks(filename, routes):
    network=Network(filename)
    results_dijikstra=[]
    results_astar=[]

    for start,end in routes:
        start_time=time.perf_counter()
        network.shortest_path(start,end)
        end_time=time.perf_counter()
        time_taken=end_time-start_time
        node=network.router.visited_nodes
        results_dijikstra.append({"time":time_taken, "node": node})

        start_time=time.perf_counter()
        network.shortest_path_astar(start,end)
        end_time=time.perf_counter()
        time_taken=end_time-start_time
        node=network.router.visited_nodes
        results_astar.append({"time":time_taken, "node": node})

    time_dijikstra, node_dijikstra = total_results(results_dijikstra)
    time_astart, node_astar = total_results(results_astar)

    print(f"-----{filename}----")
    print("dijikstra:", time_dijikstra, node_dijikstra )
    print("astart: ", time_astart, node_astar)
    print("\n")

"""
