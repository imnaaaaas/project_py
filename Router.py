from graph import Graph  
from priority_queue import PriorityQueue


#es xelit dawerilimaq gavagrdzelo ver gavige wesierad

class Router:
    def __init__(self,graph):
        self.graph=graph #referencee of graph

    def shortest(self,start,end):
        dist={start:0}
        prev={} #hasnot added were we come from
        visited =set() #shortest distance never changed

        self.pq = PriorityQueue()
        self.pq.insert(0,start) 

        while self.pq.heap: #while heap isnot empty
            w1,n1 = self.pq.extract_min() #current unused cheapest
            if n1 in visited:
                continue
            visited.add(n1)

            for edge in self.graph.neighbors(n1):
                new_dist=w1+edge.travel_time #cost to reach edge.to_stop
                if edge.to_stop not in dist or new_dist<dist[edge.to_stop]: #never record or cheaper
                    dist[edge.to_stop]=new_dist #save better 
                    prev[edge.to_stop]=n1 #where we came from

                    if edge.to_stop in self.pq.pos_map:
                        self.pq.decrease_key(edge.to_stop, new_dist)
                    else:
                        self.pq.insert(new_dist, edge.to_stop)

        if end not in dist and start!=end:
            return []


        current=end
        path=[end]
        while current in prev:
            current=prev[current]
            path.append(current)
        path=path[::-1]

        return path

        