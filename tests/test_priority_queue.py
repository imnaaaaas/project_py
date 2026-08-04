
"""test PriorityQueue  module"""
import pytest
import random
import heapq
from transit.priority_queue import PriorityQueue



def test_insert_and_pop_min():#does it return smallest 1 
    pq = PriorityQueue()
    pq.push(10, "A")
    pq.push(5, "B")
    pq.push(8, "C")

    assert pq.pop_min() == [5,"B"]
    assert pq.pop_min() == [8,"C"]
    assert pq.pop_min() == [10,"A"]



def test_pop_min_on_empty_queue(): #fail safely or crash 2
    pq = PriorityQueue()
    assert pq.pop_min() == None



def test_dublicates_extracted_correctly(): #when things are tie 3
    pq = PriorityQueue()
    pq.push(10, "A")
    pq.push(10,"B")
    pq.push(5,"C")


    first =  pq.pop_min() 
    second =pq.pop_min()
    third=pq.pop_min()

    assert first == [5,"C"]
    assert {second[1], third[1]} =={"A","B"}
    assert second[0] == 10 and third[0]==10


def test_decrease_ley_changes_extraction_order():#lower priority change extraction order(decrease_key)
    pq = PriorityQueue()
    pq.push(10, "A")
    pq.push(5, "B")
    pq.push(8, "C")

    pq.decrease_key("A",3)

    assert pq.pop_min() == [3,"A"]
    assert pq.pop_min() == [5,"B"]
    assert pq.pop_min() == [8,"C"]

def test_decrease_key_missing_elemet(): #fail visible or do undefiened 6
    pq = PriorityQueue()
    with pytest.raises(KeyError):
        pq.decrease_key("nonexistent", 1)  

def test_decrease_key_larger_value_ignored(): #equal/larger value 7 bad value
    pq = PriorityQueue()
    pq.push(5, "A")
    pq.decrease_key("A",10)
    assert pq.pop_min() == [5,"A"]


def test_strees_again_heapq(): #  8
    random.seed(42)
    items =[]
    for i in range(50):
        priority = random.randint(1,100)
        stop_id=str(i)
        items.append((priority,stop_id))

    pq = PriorityQueue()
    reference = [] 

    for priority,stop_id in items:
        pq.push(priority,stop_id)
        heapq.heappush(reference,[priority,stop_id])
    for _ in range(50):
        mine = pq.pop_min()
        heq = heapq.heappop(reference)
        assert mine == heq