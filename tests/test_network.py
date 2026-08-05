from transit.graph import load_graph_from_json
from transit.router import Router
from transit.network import Network
import pytest


def test_shortest_path_matches_router():
    graph = load_graph_from_json("network_jsons/example_network.json")
    router = Router(graph)
    network = Network("network_jsons/example_network.json")

    assert router.shortest_path("N1", "S2") == network.shortest_path("N1", "S2")


def test_shortest_path_astar_matches_router():
    graph = load_graph_from_json("network_jsons/example_network.json")
    router = Router(graph)
    network = Network("network_jsons/example_network.json")

    assert router.shortest_path_astar("N1", "S2") == network.shortest_path_astar("N1", "S2")


def test_shortest_path_with_transfers_matches_router():
    graph = load_graph_from_json("network_jsons/example_network.json")
    router = Router(graph)
    network = Network("network_jsons/example_network.json")
    
    max_transfers = 2
    assert router.shortest_path_with_transfers("N1", "S2", max_transfers) == \
        network.shortest_path_with_transfers("N1", "S2", max_transfers)

