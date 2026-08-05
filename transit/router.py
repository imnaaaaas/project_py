from transit.graph import Graph, Edge
from transit.priority_queue import PriorityQueue
import math
from utils.logger import logger


# dijikstra
class Router:
    def __init__(self, graph) -> None:
        self.graph = graph  # referencee of graph
        self.max_speed = self._average_max_speed()  # faster way roughly
        

    def shortest_dijikstra(self, start: str ,  end: str) -> list[str]:
        """Find the shortest path between start and end using Dijkstra's algorithm."""
        dist = {start: 0}
        prev = {}  # hasnot added were we come from
        visited = set()  # shortest distance never changed
        self.visited_nodes = 0

        self.pq = PriorityQueue()
        self.pq.push(0, start) 

        while self.pq.heap:  # while heap isnot empty
            weight, node = self.pq.pop_min()  # current unused cheapest
            if node in visited:
                continue
            visited.add(node)
            self.visited_nodes += 1
            if node == end:
                break

            for edge in self.graph.neighbors(node):
                new_node_cost = weight + edge.travel_time  # cost to reach edge.to_stop
            
                if edge.to_stop not in dist or new_node_cost < dist[edge.to_stop]:  # never record or cheaper
                    dist[edge.to_stop] = new_node_cost  # save better 
                    prev[edge.to_stop] = node  # where we came from

                    #
                    if edge.to_stop in self.pq.stores_ids:
                        self.pq.decrease_key(edge.to_stop, new_node_cost)
                    else:
                        self.pq.push(new_node_cost, edge.to_stop)

        if end not in dist and start != end:
            logger.warning(f"No route found from {start} to {end}") # no route found
            return []

        self.last_distance = dist.get(end, None)  # get real weights for test

        current = end
        path = [end]  # last stop_id 
        while current in prev:
            current = prev[current]
            path.append(current)
        path = path[::-1]

        return path

    def shortest_path_astar(self, start: str , end: str) -> list[str]:
        """Find the shortest path between start and end using the A* algorithm."""
        dist = {start: 0}  # G(V) real cost 
        prev = {}  # hasnot added were we come from
        visited = set()  # shortest distance never changed
        self.visited_nodes = 0
        self.pq = PriorityQueue()
        self.pq.push(0, start) 

        while self.pq.heap:  # while heap isnot empty
            weight, node = self.pq.pop_min()  # current unused cheapest
            if node in visited:
                continue
            visited.add(node)
            self.visited_nodes += 1
            if node == end:
                break

            for edge in self.graph.neighbors(node):
                new_node_cost = weight + edge.travel_time  # cost to reach edge.to_stop
            
                if edge.to_stop not in dist or new_node_cost < dist[edge.to_stop]:  # never record or cheaper
                    dist[edge.to_stop] = new_node_cost  # save better 
                    prev[edge.to_stop] = node  # where we came from

                    current_cord = self.graph.get_stop(edge.to_stop)
                    end_cord = self.graph.get_stop(end)
                    distance_to_target = self.distance_between_points(
                        current_cord.lat, current_cord.lon, end_cord.lat, end_cord.lon
                    )  # straight line
                    h_val = distance_to_target / self.max_speed  # convert km to min N1→N2, N2→N3, C→S1
                    priority = new_node_cost + h_val  # f(n)=g(n)+h(n)
                    

                    if edge.to_stop in self.pq.stores_ids:
                        self.pq.decrease_key(edge.to_stop, priority)
                    else:
                        self.pq.push(priority, edge.to_stop)

        if end not in dist and start != end:
            logger.warning(f"No route found from {start} to {end}")
            return []
 

        current = end
        path = [end]  # last stop_id 
        while current in prev:
            current = prev[current]
            path.append(current)
        path = path[::-1]

        return path


    def shortest_path_with_transfers(self, start: str , end: str , max_transfers: int = 0) -> list[str]:
        """Find the shortest path considering a maximum allowed number of transfers."""
        dist = {}
        prev = {}  # hasnot added were we come from
        visited = set()  # shortest distance never changed

        start_node = (start, None, 0)  # stop/line/transfered (reach c with different cost and line)
        dist[start_node] = 0

        self.pq = PriorityQueue()
        self.pq.push(0, start_node)  # [0, ("N1", None, 0)].

        while self.pq.heap:  # while heap isnot empty
            weight, node = self.pq.pop_min()  # current unused cheapest   
            if node in visited:
                continue
            visited.add(node)

            stop_id, current_line, transfers_used = node  # unpuch and gives names

            for edge in self.graph.neighbors(stop_id):
                if current_line is not None and edge.line_id != current_line:  # for begin
                    new_transfers = transfers_used + 1  # self.transfers_used how many transfer to reach this spot
                else:
                    new_transfers = transfers_used

                if new_transfers > max_transfers:  # transfers used > given max_transfer
                    continue 

                new_node = (edge.to_stop, edge.line_id, new_transfers)
                new_node_cost = weight + edge.travel_time  # cost to reach edge.to_stop
            
                if new_node not in dist or new_node_cost < dist[new_node]:  # never record or cheaper
                    dist[new_node] = new_node_cost  # save better 
                    prev[new_node] = node  # where we came from
                    #

                    if edge.to_stop in self.pq.stores_ids:
                        self.pq.decrease_key(new_node, new_node_cost)
                    else:
                        self.pq.push(new_node_cost, new_node)

        # get details fromtuple
        best_final_node = None
        best_cost = None
        for node in dist:
            if node[0] == end:
                if best_cost is None or dist[node] < best_cost:
                    best_cost = dist[node]
                    best_final_node = node

        if best_final_node is None:
            logger.warning(f"No route from {start} to {end} within {max_transfers} transfer(s)") #
            return []

        current = best_final_node
        path = [current[0]]  # last stop_id 
        while current in prev:
            current = prev[current]
            path.append(current[0])
        path = path[::-1]

        return path


    def distance_between_points(self, lat1: float , lon1: float , lat2: float , lon2: float ) -> float:
           """Returns distance between two point in kilometrs."""
           R = 6371 
           lat1_rad = math.radians(lat1)
           lon1_rad = math.radians(lon1)
           lat2_rad = math.radians(lat2)
           lon2_rad = math.radians(lon2)

           delta_lat = lat2_rad - lat1_rad
           delta_lon = lon2_rad - lon1_rad
           a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
           c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

           return R * c

    
    def _average_max_speed(self) -> float:  
        """Calculate max speed across graph edges."""
        # N1→N2, N2→N3, C→S1 run when router is created calcualate every edge lenght and gets biggest, fixed max_speed
        max_speed = 0
        for stop in self.graph.all_stops():  # for everystop
            for edge in self.graph.neighbors(stop.id):  # for every neighbour calculate distance/time
                to_stop = self.graph.get_stop(edge.to_stop)
                distance = self.distance_between_points(stop.lat, stop.lon, to_stop.lat, to_stop.lon)
                speed = distance / edge.travel_time  # km/min
                if max_speed < speed:
                    max_speed = speed  # takes bigest speed

        logger.debug(f"Computed max_speed = {max_speed:.3f} km/min from {len(list(self.graph.all_stops()))} stops")#
        return max_speed