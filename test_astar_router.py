import pathlib
import pytest
from graph import load_graph_from_json
from router import Router

FIXTURE = pathlib.Path(__file__).parent / "example_network.json"

@pytest.fixture
def router() -> Router:
    graph = load_graph_from_json(str(FIXTURE))
    return Router(graph)

def test_astar_w1_to_e2_stays_on_blue_line(router):
    path = router.shortest_path_astar("W1", "E2")
    assert path == ["W1", "W2",  "C", "E1", "E2"]

def test_astar_n1_to_s2_stays_on_red_line(router):
    path = router.shortest_path_astar("N1", "S2")
    assert path == ["N1" , "N2", "N3", "C", "S1","S2"]

def test_astar_same_start_and_end(router):
    path = router.shortest_path_astar("N1","N1")
    assert ["N1"]

def test_astar_after_disabling_hub(router):
    router.graph.disable_stop("C")
    path = router.shortest_path_astar("N1","S2")
    assert path == []

    #test_astar_router