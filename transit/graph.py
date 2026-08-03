"""Given module for the Transit Router intern project.

Adjacency-list graph with weighted, labeled directed edges. Stops and edges
can be disabled at runtime; `neighbors()` transparently skips them so
routing algorithms do not need to know about outages.

Do NOT modify this file. Treat it as a library.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True)
class Stop:
    id: str
    name: str
    lat: float
    lon: float


@dataclass(frozen=True)
class Edge:
    from_stop: str
    to_stop: str
    travel_time: float
    line_id: str


class Graph:
    """Adjacency-list graph with weighted, labeled, directed edges.

    - Edges are directed. If you want bidirectional behavior, add both directions.
    - Multiple edges between the same pair of stops are allowed (one per line).
    - Disabling a stop or edge is a cheap flag flip — no rebuild required.
    """

    def __init__(self) -> None:
        self._stops: dict[str, Stop] = {}  #all stop exist
        self._out_edges: dict[str, list[Edge]] = defaultdict(list) #all edge exist
        self._disabled_stops: set[str] = set() #currently turned off stops
        self._disabled_edges: set[tuple[str, str, str]] = set() #(from, to, line_id)/ currently turned off edge

    #add vertex error if you try duplicate
    def add_stop(self, stop: Stop) -> None:
        if stop.id in self._stops:
            raise ValueError(f"stop {stop.id!r} already exists")
        self._stops[stop.id] = stop

    #Adds edge, but first checks both endpoints already exist as stops
    def add_edge(self, edge: Edge) -> None:
        if edge.from_stop not in self._stops:
            raise ValueError(f"unknown from_stop {edge.from_stop!r}")
        if edge.to_stop not in self._stops:
            raise ValueError(f"unknown to_stop {edge.to_stop!r}")
        self._out_edges[edge.from_stop].append(edge)

    def get_stop(self, stop_id: str) -> Stop:
        return self._stops[stop_id]

    def all_stops(self) -> Iterable[Stop]:
        return self._stops.values()


    #routing algorithm instead touch out_edge
    def neighbors(self, stop_id: str) -> Iterator[Edge]:
        """Yield outgoing edges from `stop_id`, skipping disabled edges and
        edges whose endpoint is a disabled stop. Yields nothing if `stop_id`
        itself is disabled.
        """
        if stop_id in self._disabled_stops:
            return #stop disable retunr nothing
        for edge in self._out_edges.get(stop_id, ()):
            if edge.to_stop in self._disabled_stops:
                continue #skip destination is cancelled
            if (edge.from_stop, edge.to_stop, edge.line_id) in self._disabled_edges:
                continue #skip line is canceled
            yield edge #safe edges

    def disable_stop(self, stop_id: str) -> None:
        if stop_id not in self._stops:
            raise KeyError(stop_id)
        self._disabled_stops.add(stop_id)

    def enable_stop(self, stop_id: str) -> None:
        self._disabled_stops.discard(stop_id)

    def disable_edge(self, from_id: str, to_id: str, line_id: str) -> None:
        self._disabled_edges.add((from_id, to_id, line_id))

    def enable_edge(self, from_id: str, to_id: str, line_id: str) -> None:
        self._disabled_edges.discard((from_id, to_id, line_id))


def load_graph_from_json(path: str) -> Graph:
    """Load a Graph from a JSON file with the shape used by example_network.json."""
    with open(path) as f:
        data = json.load(f)
    graph = Graph()
    for s in data["stops"]:
        graph.add_stop(Stop(id=s["id"], name=s["name"], lat=s["lat"], lon=s["lon"]))
    for e in data["edges"]:
        graph.add_edge(
            Edge(
                from_stop=e["from"],
                to_stop=e["to"],
                travel_time=e["travel_time"],
                line_id=e["line_id"],
            )
        )
    return graph
