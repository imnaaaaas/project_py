# Design Document — Transit Route Planne

## 1. Overview
    Program solves problem to go from station A to station B with shortest path weights.
    On example, given small city transit network, given start and destination stop, and program return fastest route.
    Implemented algorithms:
    -Dijkstra's algorithm using your priority queue.
    -A* using **haversine** straight-line distance as the heuristic.
    -DP for the transfer-constrained variant

## 2. Class Responsibilities
    
### Graph(given)
    Graph- given file, which owns raw network data and outage edges(disabled stops/edges). 
    neighbors() method which telling us where we can go from current stop.(outgoing edges)

### PriorityQueue
    PriorityQueue - using data structure Binary min-heap with decrease_key as priority queue.
    Code manages add item, extract minimum item. Make correct Binary min-heap logic.PriorityQueue is frontier for Dijkstra,A* which are pathfinding algorithms.When Dijkstra works on data PriorityQueueacts as the core engine that tells  which station to visit next.

### Router
    Router - owns Dijkstra, A*, transfer-constrained DP.
    Dijkstra - works on real weights and return shortest path from start to end.


    A*  using heuristic (f(v)=g(v)+h(v)).On this example, i write h(v) as average time(km/min) between nodes.
    (I add two method  distance_between_points and _average_max_speed. distance_between_points calculates km between nodes by using lan/lon which is given in json.When Router is created  average_max_speed is calculated permanently and saved in constructor as fixed number.we use distance_between_points in this method for calculate speed. we get distance and devide into real time between nodes(travel_time) which is given in json. and we choose max among them and this will be average maxsimum speed.In A* algorithm we calculate average time using those 2 methods, h(v)= distance to target node calculated devided on average max speded.)
    transfer-constrained DP - using dijkstraiji algorithm. Different from Dijkstra code is we insert (real_weight,(start_node,current_line,transfer_used)). By this way it become more easy to check where we came from, last node line_id and if it changed line to reach current node.

### Network
    Network - is thin wrapper,  loads from JSON, holds a `Graph`, exposes the routing API. I use composition, and call all the methods from files i have created. It owns Graph and Router, and expose one clean, simple interface, for CLI. I write this way because CLI never need to know Graph/Router exists seperately
    

### CLI
    CLI(__main__.py) runnable file which parses arguments, builds Network, calls its methods and prints results.
    



##  3. Complexity Analysis
    PriorityQueue -  insert O(logn) / extract O(logn) / decrease_key O(logn)
    space O(N) (stores_ids)

    Router - Dijkstra/A* time - O((V+E) log V) / E*O(logV)   space- O(V)
            max_tranfer  time - O((V×K + E×K) log(V×K)) k=max_transfer+1 (max transfer is calculated on every iteration)
    
    Benchmark - time - O(R \(V + N) \log V) (nodes/edge/route) space O(Nmax + Emax) 
    




## 4. Benchmarks

2026-08-04 18:16:17,026 - INFO - -----network_jsons/example_network_100.json-----
2026-08-04 18:16:17,026 - INFO - dijkstra: 0.000590s 180 nodes
2026-08-04 18:16:17,026 - INFO - astar: 0.000572s 108 nodes
2026-08-04 18:16:17,026 - INFO -
2026-08-04 18:16:17,053 - INFO - -----network_jsons/example_network_1000.json-----
2026-08-04 18:16:17,053 - INFO - dijkstra: 0.005484s 1493 nodes
2026-08-04 18:16:17,053 - INFO - astar: 0.003447s 798 nodes
2026-08-04 18:16:17,053 - INFO -
2026-08-04 18:16:17,388 - INFO - -----network_jsons/example_network_10000.json-----
2026-08-04 18:16:17,388 - INFO - dijkstra: 0.089882s 18456 nodes
2026-08-04 18:16:17,388 - INFO - astar: 0.062870s 11070 nodes

The test results shows that A* is always faster and check less nodes than Dijikstra on every network size.
This shows that heuristic works correctly in real world,saving actual time and computer.


## 5. A* Heuristic: Admissibility

write heuristic must be less than true cost to goal

A* heuristic h(v) is admissible if it never overestimates the true cost to reach the goal from any node. 
h(v)<true_cost(v,goal)

Program calculating straight-line distance on map using GPS coordinats(lat,lon), and divides it by max possible speed in network. Straight line is always shortests possible distance between two points, and max speed gives fastersts possible time,
our guess is always optimistic. If our guess was too high than real cost, A* think that good path is expensive and skip it by mistake.In this way A* would give a wrong, longer route instead of actual shortest path.
In test (test_astar_heuristic_is_admissible) its calculating straight-line distance for every node to end, and then compare to their real cost to prove that heuristic is Admissibility.



