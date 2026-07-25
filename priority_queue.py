

class PriorityQueue:
    def __init__(self):
        self.heap=[]
        self.pos_map={}#stores  stop_id

    def insert(self,distance,stop_id):#add new value and bubble it
        self.heap.append([distance, stop_id])
        last_ind=len(self.heap)-1
        self.pos_map[stop_id]=last_ind #new added index
        self._init_up(last_ind)


    def _init_up(self,ind):#for minheap parent<son and swap
        
        while ind>0:
            parent_ind=(ind-1)//2
            id_a = self.heap[ind][1]#chils id [priority, id]
            id_b= self.heap[parent_ind][1]#parents id 
            if self.heap[ind]<self.heap[parent_ind]:
                self.heap[ind] , self.heap[parent_ind] = self.heap[parent_ind], self.heap[ind]
                self.pos_map[id_a]=parent_ind #make them correct index
                self.pos_map[id_b]=ind
                ind=parent_ind #after swap for loop condition
            else:
                break

    def extract_min(self): #es kargad gaviaro
        if not self.heap:
            return None #test 2
        if len(self.heap)==1:
            item = self.heap.pop()#item is id
            del self.pos_map[item[1]] #del no longer exists
            return item

        min_val = self.heap[0] #get 0 index whole pair which is min
        del self.pos_map[min_val[1]] #del id from that pair
        self.heap[0]=self.heap.pop() #last on 0ind
        self.pos_map[self.heap[0][1]]=0 #give 0 index pair id =0
        self._sift_down(0) #restore pushing 0
        return min_val #return min
            

    def _sift_down(self,ind): 
#for left right child, new addded smallest compare to them for minHeap
        n=len(self.heap)
        while True:
            smallest=ind
            right=2*ind+2
            left=2*ind+1
            if left<n and self.heap[left]<self.heap[smallest]:
                smallest=left
            if right<n and self.heap[right]<self.heap[smallest]:
                smallest=right
            if smallest !=ind:
                id_a=self.heap[ind][1]
                id_b=self.heap[smallest][1]
                self.heap[ind], self.heap[smallest] = self.heap[smallest], self.heap[ind]
                self.pos_map[id_a]=smallest
                self.pos_map[id_b]=ind
                ind=smallest
            else:
                break
            
    def decrease_key(self,stop_id,new_val):#use hashmap
        if stop_id not in self.pos_map:
            raise KeyError(f"{stop_id} not found") #test 6
        ind=self.pos_map[stop_id]
        current_val=self.heap[ind][0]
        if new_val >= current_val:
            return 
        self.heap[ind]=[new_val, stop_id]
        self._init_up(ind)

    


"""
5 method 
insert
extrac_min
decrease_key working
decrease_key missing value
decrease_key bad new value
"""

