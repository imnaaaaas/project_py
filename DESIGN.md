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
    Code manages add item, extract minimum item. Make correct Binary min-heap logic.

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
        
    




