import pathlib
import pytest
from transit.graph import load_graph_from_json
from transit.router import Router

FIXTURE = pathlib.Path(__file__).parent / "example_network.json"
FIXTURE_EXTENDED = pathlib.Path(__file__).parent / "example_network2.json"

@pytest.fixture
def router() -> Router:
    graph = load_graph_from_json(str(FIXTURE))
    return Router(graph)

@pytest.fixture
def router_extended() -> Router:
    graph = load_graph_from_json(str(FIXTURE_EXTENDED))
    return Router(graph)




def test_transfers_zero_on_original_network_returns_no_route(router):
    path = router.shortest_path_with_transfers("N1", "E2", max_transfers=0)
    assert path == []

def test_transfers_zero_on_extended_network_finds_green_route(router_extended):
    path = router_extended.shortest_path_with_transfers("N1", "E2", max_transfers=0)
    assert path == ["N1", "G1", "G2", "E2"]

def test_transfers_one_on_extended_network_finds_faster_route(router_extended):
    path = router_extended.shortest_path_with_transfers("N1", "E2", max_transfers=1)
    assert path == ["N1", "N2", "N3", "C", "E1", "E2"]

def test_transfers_unlimited_matches_plain_dijkstra_result(router_extended):
    dijkstra_path = router_extended.shortest_dijikstra("N1", "E2")
    transfers_path = router_extended.shortest_path_with_transfers("N1", "E2", max_transfers=10)
    assert dijkstra_path == transfers_path

def test_transfers_same_start_and_end(router):
    path = router.shortest_path_with_transfers("N1", "N1", max_transfers=1)
    assert path == ["N1"]


def test_transfers_zero_on_single_line_route_needs_no_transfer(router):
    path = router.shortest_path_with_transfers("N1", "S2", max_transfers=0)
    assert path == ["N1","N2","N3","C","S1","S2"]
