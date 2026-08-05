"""Tests for the given Graph module.

Doubles as a usage example — read this file to see how to call every part
of the API before you start writing your own code.

Run with:  pytest test_graph.py -v
"""

import pathlib

import pytest


from transit.graph import Edge, Graph, Stop, load_graph_from_json

FIXTURE = pathlib.Path(__file__).parent.parent / "network_jsons/example_network.json"

@pytest.fixture
def graph() -> Graph:
    return load_graph_from_json(str(FIXTURE))


def test_all_stops_loaded(graph: Graph) -> None:
    ids = {s.id for s in graph.all_stops()}
    assert ids == {"N1", "N2", "N3", "C", "S1", "S2", "W1", "W2", "E1", "E2"}


def test_get_stop_returns_full_stop(graph: Graph) -> None:
    hub = graph.get_stop("C")
    assert hub.name == "Central Hub"
    assert hub.lat == 40.74
    assert hub.lon == -74.00


def test_neighbors_of_hub_has_four_edges(graph: Graph) -> None:
    # C is the transfer hub: 2 outgoing red edges + 2 outgoing blue edges
    edges = list(graph.neighbors("C"))
    assert len(edges) == 4
    by_line: dict[str, int] = {}
    for e in edges:
        by_line[e.line_id] = by_line.get(e.line_id, 0) + 1
    assert by_line == {"red": 2, "blue": 2}


def test_disable_stop_removes_all_edges_through_it(graph: Graph) -> None:
    assert len(list(graph.neighbors("C"))) == 4
    assert len(list(graph.neighbors("N3"))) == 2

    graph.disable_stop("C")

    # C yields nothing
    assert list(graph.neighbors("C")) == []
    # N3 no longer sees its edge to C; only the northbound edge to N2 remains
    n3_targets = [e.to_stop for e in graph.neighbors("N3")]
    assert n3_targets == ["N2"]


def test_enable_stop_restores_full_connectivity(graph: Graph) -> None:
    graph.disable_stop("C")
    graph.enable_stop("C")
    assert len(list(graph.neighbors("C"))) == 4


def test_disable_edge_is_directional(graph: Graph) -> None:
    graph.disable_edge("C", "E1", "blue")

    # C -> E1 is gone
    targets_from_c = [(e.to_stop, e.line_id) for e in graph.neighbors("C")]
    assert ("E1", "blue") not in targets_from_c

    # but E1 -> C still works (reverse direction is a separate edge)
    assert any(e.to_stop == "C" for e in graph.neighbors("E1"))


def test_disable_edge_is_line_specific(graph: Graph) -> None:
    # Disabling a nonexistent (from, to, line) triple is a harmless no-op.
    graph.disable_edge("C", "E1", "red")  # there is no red edge C -> E1
    # blue C -> E1 must still be there
    targets = [(e.to_stop, e.line_id) for e in graph.neighbors("C")]
    assert ("E1", "blue") in targets


def test_add_edge_with_unknown_endpoint_raises() -> None:
    g = Graph()
    g.add_stop(Stop(id="A", name="A", lat=0.0, lon=0.0))
    with pytest.raises(ValueError):
        g.add_edge(Edge(from_stop="A", to_stop="B", travel_time=1.0, line_id="x"))


def test_duplicate_stop_raises() -> None:
    g = Graph()
    g.add_stop(Stop(id="A", name="A", lat=0.0, lon=0.0))
    with pytest.raises(ValueError):
        g.add_stop(Stop(id="A", name="A", lat=0.0, lon=0.0))


def test_disable_unknown_stop_raises(graph: Graph) -> None:
    with pytest.raises(KeyError):
        graph.disable_stop("does-not-exist")


def test_multiple_edges_between_same_stops_allowed() -> None:
    g = Graph()
    g.add_stop(Stop("A", "A", 0.0, 0.0))
    g.add_stop(Stop("B", "B", 0.0, 0.0))
    g.add_edge(Edge("A", "B", 5.0, "red"))
    g.add_edge(Edge("A", "B", 3.0, "blue"))
    edges = list(g.neighbors("A"))
    assert len(edges) == 2
    assert {e.line_id for e in edges} == {"red", "blue"}
