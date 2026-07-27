"""#dijiskstra algorithm
import heapq
class Solution:
    def shortestPath(self,n,edges,start): 
#n how many spot, src where we start, edges=[[start,stop,weight]]
        adj={}
        for i in range(n):
            adj[i]=[]
        
        for s,d, weight in edges:
            adj[s].append([d,weight])

        shortest={}
        minHeap=[[0,src]]

        while minHeap:
            w1,n1 = heapq.heappop(minHeap)
            if n1 in shortest:
                continue
            shortest[n1]=w1

            for n2,w2 in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap,[w1+w2,n2]) #it allow one vertex can have multiple entry
        for i in range(n):
            if i not in shortest:
                shortest=i =-1
        return shortest

    
s=Solution()

print(s.shortestPath(5,[[0,1,10],[0,2,3],[1,3,2],[2,1,4],[2,3,8],[2,4,2],[3,4,5]], 0))
  


!!!!!!!!!!!!!

es kargad gaviaro, magalitebze
kitxvebi meore kompiuteridan gadmovitano
        
"""

import heapq
class Solution:
    def shortestPath(self,n,edges,src):
        adj={}
        for i in range(n):
            adj[i]=[]

        for s,d, weight in edges:
            adj[s].append([d,weight])

        shortest={}
        minHeap=[[0,src]]
        while minHeap:
            w1,n1 = heapq.heappop(minHeap)
            if n1 in shortest:
                continue
            shortest[n1]=w1

            for n2,w2 in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap,[w1+w2,n2])
        for i in range(n):
            if i not in shortest:
                shortest[i]=-1
        return shortest

s=Solution()


print(s.shortestPath(5,[[0,1,10],[0,2,3],[1,3,2],[2,1,4],[2,3,8],[2,4,2],[3,4,5]], 0))
  

"""
import heapq
import random
 
class MinHeap:
    def __init__(self):
        self.heap=[]

    def insertion(self,val):
        self.heap.append(val) #put value at end
        last_inx=len(self.heap)-1 #get index of that added
        self._init_up(last_inx) #buble from last index

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap)==1:
            return self.heap.pop()

        min_val=self.heap[0]  #min at 0
        self.heap[0]= self.heap.pop() #last on 0 index
        self._sift_down(0) #restore pushing 0
        return min_val #return min
            
    def _sift_down(self,ind):
        n=len(self.heap)
        while True:
            smallest=ind
            right=2*ind+2
            left=2*ind+1
            if left < n and self.heap[left]<self.heap[smallest]:
                smallest=left

            if right<n and self.heap[right]<self.heap[smallest]:
                smallest=right

            if smallest != ind:
                self.heap[ind], self.heap[smallest]= self.heap[smallest],self.heap[ind],
                
                ind=smallest
            else:
                break


            

    def _init_up(self,ind):
        while ind>0:
            parent_ind = (ind-1)//2
            #if parent is smaller swap
            if self.heap[ind]<self.heap[parent_ind]:
                self.heap[ind], self.heap[parent_ind]= self.heap[parent_ind],self.heap[ind]
                
                ind=parent_ind
            else:
                break


def test_min_heap():
    my_heap = MinHeap()
    std_heap = []
    data = [random.randint(-1000, 1000) for _ in range(1000)]
    for x in data:
        my_heap.insertion(x)
        heapq.heappush(std_heap, x)
    for _ in range(len(data)):
        m1 = my_heap.extract_min()
        m2 = heapq.heappop(std_heap)
        assert m1 == m2, f"Mismatch! Custom: {m1}, Standard: {m2}"
    print("✅ All 1,000 extractions matched standard heapq!")
if __name__ == "__main__":
    test_min_heap()
"""

""" with decrease_key
class MinHeap:
    def __init__(self):
        self.heap=[]
        self.pos_map={} #map item - index in self.heap hashmap

    def swap(self, i,j):#swap elements and updatee position map
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos_map[self.heap[i][0]]=i
        self.pos_map[self.heap[j][0]]=j

    def insertion(self, item, key_val):
        #stores elements as tuple(item,key_val)
        if item in self.pos_map:
            raise ValueError("already exists")
        ind=len(self.heap)
        self.heap.append((item, key_val))
        self.pos_map[item]=ind
        self._sift_up(ind)

    def decrease_key(self,item,new_val):
        if item not in self.pos_map:
            raise KeyError("item not found")
        ind = self.pos_map[item]
        current_val=self.heap[ind][1]
        if new_val >= current_val:
            return #decrease ignore if new_val is larger
        self.heap[ind]=(item,new_val)#update value in place
        self._sift_up(ind)#buble to restore min_heap

    def _sift_up(self,ind):
        while ind>0:
            parent_ind=(ind-1)//2
            if self.heap[ind][1] < self.heap[parent_ind][1]:
                self._swap(ind,parent_ind)
                ind=parent_ind
            else:
                break
                


----


    def __init__(self,graph):
        self.graph=graph

    def shortestpath(self,start,end): #start/destination id  
        dist={start:0}
        prev={} #which current node hasnt added yet
        visited = set()


        self.pq = PriorityQueue() #same idea as minHeap
        self.pq.insert(0,start)

        while  self.pq.heap:#still smth in queue 

            w1,n1= self.pq.extract_min() #current unprocesed cheapest
            if n1 in visited:
                continue
            visited.add(n1)

            for edge in self.graph.neighbors(n1):
                new_dist=w1+edge.travel_time # candidate to reach / cost to reach edge.to_stop
                if edge.to_stop not in dist or new_dist<dist[edge.to_stop]: #never recorded or its cheaper
                    dist[edge.to_stop]=new_dist #save better distance
                    prev[edge.to_stop]=n1 #where we came from

                if edge.to_stop in self.pq.pos_map: #check stop is already in queue
                    self.pq.decrease_key(edge.to_stop,new_dist)
                else:
                    self.pq.insert(new_dist,edge.to_stop)
    
        
        current=end
        path=[end]
        while current   in prev:
            current=prev[current]
            path.append(current)
            path=path[::-1]

        return path

 


    """


