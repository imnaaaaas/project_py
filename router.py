from graph import Graph  
from priority_queue import PriorityQueue
import math

#dijikstra
class Router:
    def __init__(self,graph):
        self.graph=graph #referencee of graph
        self.max_speed=self._compute_max_speed() #faster way roughly
        

    def _compute_max_speed(self):  
            #N1→N2, N2→N3, C→S1 run when router is created calcualate every edge lenght and gets biggest, fixed max_speed
            max_speed=0
            for stop in self.graph.all_stops(): #for everystop
                for edge in self.graph.neighbors(stop.id): #for every neighbour calculate distance/time
                    to_stop = self.graph.get_stop(edge.to_stop)
                    distance = self.distance_between_points(stop.lat, stop.lon, to_stop.lat, to_stop.lon)
                    speed = distance /edge.travel_time #km/min
                    if max_speed<speed:
                        max_speed=speed #takes bigest speed
            return max_speed

    
    def shortest_dijikstra(self,start,end):
        dist={start:0}
        prev={} #hasnot added were we come from
        visited =set() #shortest distance never changed

        self.pq = PriorityQueue()
        self.pq.insert_item(0,start) 

        while self.pq.heap: #while heap isnot empty
            weight,node = self.pq.extract_min() #current unused cheapest
            if node in visited:
                continue
            visited.add(node)

            for edge in self.graph.neighbors(node):
                new_node_cost=weight+edge.travel_time #cost to reach edge.to_stop
            
                if edge.to_stop not in dist or new_node_cost<dist[edge.to_stop]: #never record or cheaper
                    dist[edge.to_stop]=new_node_cost #save better 
                    prev[edge.to_stop]=node #where we came from
                    #

                    if edge.to_stop in self.pq.stores_ids:
                        self.pq.decrease_key(edge.stores_ids, new_node_cost)
                    else:
                        self.pq.insert_item(new_node_cost, edge.to_stop)

        if end not in dist and start!=end:
            return []


        current=end
        path=[end] #last stop_id 
        while current in prev:
            current=prev[current]
            path.append(current)
        path=path[::-1]

        return path



    def shortest_path_astar(self, start, end):
        dist={start:0} #G(V) real cost 
        prev={} #hasnot added were we come from
        visited =set() #shortest distance never changed

        self.pq = PriorityQueue()
        self.pq.insert_item(0,start) 

        while self.pq.heap: #while heap isnot empty
            weight,node = self.pq.extract_min() #current unused cheapest
            if node in visited:
                continue
            visited.add(node)

            for edge in self.graph.neighbors(node):
                new_node_cost=weight+edge.travel_time #cost to reach edge.to_stop
            
                if edge.to_stop not in dist or new_node_cost<dist[edge.to_stop]: #never record or cheaper
                    dist[edge.to_stop]=new_node_cost #save better 
                    prev[edge.to_stop]=node #where we came from

                    current_cord= self.graph.get_stop(edge.to_stop)
                    end_cord = self.graph.get_stop(end)
                    distance_to_target = self.distance_between_points(current_cord.lat,current_cord.lon,end_cord.lat,end_cord.lon) #straight line
                    h_val= distance_to_target/self.max_speed  #convert km to min N1→N2, N2→N3, C→S1
                    priority = new_node_cost+h_val
                    

                    if edge.to_stop in self.pq.stores_ids:
                        self.pq.decrease_key(edge.to_stop, priority)
                    else:
                        self.pq.insert_item(priority, edge.to_stop)

        if end not in dist and start!=end:
            return []


        current=end
        path=[end] #last stop_id 
        while current in prev:
            current=prev[current]
            path.append(current)
        path=path[::-1]

        return path


    
    def distance_between_points(self,lat1,lon1, lat2,lon2):# returns distance between two point in kilometrs

        R = 6371 
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        delta_lat=lat2_rad-lat1_rad
        delta_lon=lon2_rad-lon1_rad
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c
    
    

# time complexity O(V+E(logV)) / O(ElogV)
# space O(V) / O(N)
