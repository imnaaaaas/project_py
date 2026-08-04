

class PriorityQueue:
    def __init__(self):
        self.heap=[]
        self.stores_ids={}#stores  stop_id


    def push(self,distance,stop_id):#add new value and bubble it
        """Add a new value and bubble it up to maintain heap order."""
        self.heap.append([distance, stop_id])
        last_ind= len(self.heap) -1
        self.stores_ids[stop_id] = last_ind #new added index
        self._insertion_init_up(last_ind)


    def pop_min(self):
        """Remove and return the minimum element from the priority queue."""
        if not self.heap:
            return None #test 2
        if len(self.heap) == 1:
            item = self.heap.pop()#item is id
            del self.stores_ids[item[1]] #del no longer exists
            return item

        min_value = self.heap[0] #get 0 index whole pair which is min
        del self.stores_ids[min_value[1]] #del id from that pair
        self.heap[0] = self.heap.pop() #last becomes first
        self.stores_ids[self.heap[0][1]]=0 #first id =0
        self._extract_sift_down(0) #restore pushing 0
        return min_value #return min
            
       
    def decrease_key(self,stop_id,new_val):#use hashmap
        """Decrease the priority value of a given stop_id."""
        if stop_id not in self.stores_ids:
            raise KeyError(f"{stop_id} not found") #test 6
        ind = self.stores_ids[stop_id]
        current_value = self.heap[ind][0]
        if new_val >= current_value:
            return 
        self.heap[ind] = [new_val, stop_id]
        self._insertion_init_up(ind)


    def _extract_sift_down(self,ind):
        """Restore heap property by shifting an element down."""
        length = len(self.heap)
        while True:
              smallest = ind
              right_index = 2 * ind + 2
              left_index = 2 * ind + 1
              if left_index < length and self.heap[left_index] < self.heap[smallest]:
                  smallest = left_index
              if right_index < length and self.heap[right_index] < self.heap[smallest]:
                  smallest = right_index
              if smallest != ind:
                  id_parent = self.heap[ind][1]
                  id_child = self.heap[smallest][1]
                  self.heap[ind], self.heap[smallest] = self.heap[smallest], self.heap[ind]
                  self.stores_ids[id_parent] = smallest #update stores_ids
                  self.stores_ids[id_child] = ind
                  ind = smallest
              else:
                  break
         
    def _insertion_init_up(self,ind):#for minheap parent<son and swap
        """Restore heap property by shifting an element up."""
        while ind > 0:
            parent_ind =(ind - 1) // 2
            id_child = self.heap[ind][1]#chils id [priority, id]
            id_parent = self.heap[parent_ind][1]#parents id 
            if self.heap[ind] < self.heap[parent_ind]:
                self.heap[ind], self.heap[parent_ind] = self.heap[parent_ind], self.heap[ind]
                self.stores_ids[id_child] = parent_ind #make them correct index
                self.stores_ids[id_parent] = ind
                ind=parent_ind #after swap for loop condition
            else:
                break
    


"""
5 method 
insert
extrac_min
decrease_key working with cheaper value
decrease_key missing value
decrease_key bad new value

insert O(logn)
extract O(logn)
decrease_key O(logn)
space O(N)
"""

