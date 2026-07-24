# Intern Project: Mini Transit Route Planner

## Overview
Build a route planner over a small city transit network (bus, tram, subway). Given a start and destination stop, return the fastest route, optionally constrained by the number of transfers. This project exercises graphs, shortest-path algorithms, priority queues, dynamic programming, OOP design, and rigorous complexity analysis.

- **Duration:** 2 weeks
- **Language:** Python 3.10+
- **Deliverable:** importable package + CLI demo + tests + short design write-up

## Learning goals
- Read and use a non-trivial given API (a `Graph` class with adjacency list + weighted labeled edges) without modifying it
- Implement a binary min-heap priority queue from scratch, with `decrease_key`
- Implement Dijkstra and A* shortest-path algorithms from scratch
- Use dynamic programming to solve a constrained shortest-path variant
- Reason about heuristic admissibility in A* and what happens when it fails
- Write idiomatic OOP Python with clear responsibilities per class
- Analyze and document time and space complexity

## What is given vs. what you build
- **Given** (do not modify):
  - [graph.py](graph.py) — `Stop`, `Edge`, `Graph` classes + `load_graph_from_json`. Full API in [Provided API](#provided-api) below.
  - [example_network.json](example_network.json) — a small 10-stop, 2-line network for smoke tests.
  - [test_graph.py](test_graph.py) — tests for the given module; **read this first** to learn the API by example.
- **You build:** `PriorityQueue`, `Router` (Dijkstra + A* + transfer-constrained DP), `Network` (thin wrapper), and the CLI.

## Functional requirements
1. Load a transit network from JSON: stops (with coordinates) and edges (with travel time and line id).
2. `shortest_path(start, end)` — return the fastest route as an ordered list of stops.
3. `shortest_path_astar(start, end)` — same as above but using A* with a geographic heuristic.
4. `shortest_path_with_transfers(start, end, max_transfers)` — fastest route using at most `max_transfers` line changes.
5. Support disabling stops or edges at runtime to simulate outages, without a full rebuild.
6. CLI demo: `python -m transit --network city.json route "A Station" "B Station"`.

## Technical requirements

### Data structures
- **Graph** — *given* (see [Provided API](#provided-api)). Use it as-is.
- **Binary min-heap** with `decrease_key` as the priority queue — implement from scratch. Do **not** use `heapq` for the core; you may use it in tests to cross-check.
- *Optional stretch:* Fibonacci heap.

### Algorithms
- Dijkstra's algorithm using your priority queue.
- A* using **haversine** straight-line distance as the heuristic.
- DP for the transfer-constrained variant — state = `(stop, transfers_used)`.
- Path reconstruction from a predecessor map.

### OOP design
Class layout:
- `Stop` — id, name, latitude, longitude *(given)*
- `Edge` — from_stop, to_stop, travel_time, line_id *(given)*
- `Graph` — `add_stop`, `add_edge`, `neighbors`, `disable_stop`, `disable_edge` *(given)*
- `PriorityQueue` — `push`, `pop_min`, `decrease_key` *(you)*
- `Router` — `shortest_path`, `shortest_path_astar`, `shortest_path_with_transfers` *(you)*
- `Network` — loads from JSON, holds a `Graph`, exposes the routing API *(you)*

The `Graph` does not know that `Router` exists — do not add algorithm code to it. Adding a new algorithm should not require changing `Graph`.

## Provided API
You will be handed a working module. **Do not modify it** — treat it as a library. The public surface:

```python
class Stop:
    id: str
    name: str
    lat: float
    lon: float

class Edge:
    from_stop: str        # Stop id
    to_stop: str          # Stop id
    travel_time: float    # minutes
    line_id: str          # e.g. "red", "blue"

class Graph:
    def add_stop(self, stop: Stop) -> None: ...
    def add_edge(self, edge: Edge) -> None: ...
    def get_stop(self, stop_id: str) -> Stop: ...
    def neighbors(self, stop_id: str) -> Iterable[Edge]:
        """Yield outgoing edges from stop_id, skipping any disabled edges
        and edges whose endpoint is a disabled stop."""
    def disable_stop(self, stop_id: str) -> None: ...
    def enable_stop(self, stop_id: str) -> None: ...
    def disable_edge(self, from_id: str, to_id: str, line_id: str) -> None: ...
    def enable_edge(self, from_id: str, to_id: str, line_id: str) -> None: ...
    def all_stops(self) -> Iterable[Stop]: ...

def load_graph_from_json(path: str) -> Graph: ...
```

Notes:
- Edges are **directed** — the JSON lists both directions explicitly. This is intentional; do not assume symmetry.
- Multiple edges between the same two stops are allowed (one per line).
- `neighbors()` handles the disabled-state filtering for you — your algorithms do not need to check it.

## Example network
A small hand-built network for smoke tests lives in [example_network.json](example_network.json). It has two crossing lines that meet at one transfer hub — enough to exercise plain Dijkstra, transfer-constrained routing, and A* with the geographic heuristic.

```
      N1 (North Terminal)
       │  red
      N2 (North Park)
       │  red
      N3 (Uptown)
       │  red
W1 ── W2 ── C ── E1 ── E2      (blue, east-west)
              │  red
             S1 (Midtown)
              │  red
             S2 (South Terminal)
```

Sanity checks you should be able to verify against this network:
- `shortest_path("N1", "S2")` follows the red line the whole way — no transfers needed.
- `shortest_path("W1", "E2")` follows the blue line the whole way — no transfers needed.
- `shortest_path("N1", "E2")` requires exactly one transfer at `C` (Central Hub).
- `shortest_path_with_transfers("N1", "E2", max_transfers=0)` returns no route.
- Disabling stop `C` disconnects the red and blue lines — cross-line routes become unreachable.

## Milestones

### Week 1 — Understand the given graph, build the priority queue, implement Dijkstra
| Day | Task |
|-----|------|
| 1   | Read the provided `Graph` module end-to-end. Write tests that load `example_network.json` and exercise `neighbors`, `disable_stop`, `disable_edge`. Verify the sanity-check queries listed above by hand. |
| 2–3 | Priority queue with `decrease_key`; tests including duplicate priorities, `decrease_key` on a missing element, and stress tests against `heapq` on random inputs |
| 4–5 | Dijkstra + path reconstruction against `example_network.json`; CLI skeleton |

### Week 2 — A*, DP variant, polish
| Day  | Task |
|------|------|
| 6–7  | A* with haversine heuristic; write a test that proves admissibility |
| 8    | DP for max-transfers-constrained routing |
| 9    | Benchmarks: Dijkstra vs. A* — query latency and nodes expanded on 100 / 1000 / 10000-stop networks |
| 10   | Complexity write-up, README, code-review polish |

## Deliverables
1. Python package matching the class layout above.
2. Test suite (`pytest`) with >80% coverage on core logic. Include graph fixtures: linear, cyclic, disconnected, and a small hand-drawn network with known optimal routes.
3. CLI demo runnable against a provided synthetic city network.
4. **`DESIGN.md`** covering:
   - Class responsibilities and why they are drawn this way.
   - Big-O complexity of every public method, with justification.
   - Benchmark table: query latency and nodes expanded for Dijkstra vs. A* on 100 / 1000 / 10000-stop networks.
   - Why the A* heuristic is admissible — and what would happen if it weren't.

## Stretch goals (pick one)
- **Bidirectional Dijkstra** — search from both ends until the frontiers meet.
- **Contraction hierarchies** for large-network speedup.
- **Multi-criteria routing** — jointly minimize time + walking distance + fare.
- Serve the API over HTTP and render routes on a Leaflet map.

## Evaluation rubric
| Area | What we look for |
|------|------------------|
| Correctness | Routes are actually optimal; edge cases handled (unreachable, same start/end, disabled stops, single-stop network) |
| Complexity | Code matches claimed Big-O; priority queue operations are truly O(log n) |
| Design | `Graph` and `Router` are decoupled; adding an algorithm doesn't require touching the graph |
| Testing | Meaningful tests including negative cases (unreachable, cycles, disabled edges) |
| Communication | A new engineer can read `DESIGN.md` and understand the tradeoffs |
| Code quality | Type hints, docstrings on public methods, PEP 8, no dead code |

## Suggested reading
- Sedgewick & Wayne, *Algorithms* — chapters on graphs and shortest paths
- Russell & Norvig, *Artificial Intelligence: A Modern Approach* — A* and heuristics
- CLRS — Dijkstra's algorithm and analysis

## Getting started
1. Fork the starter repo (or create a fresh one) and set up `pyproject.toml` with `pytest`, `mypy`, and `ruff`. Drop the provided `graph.py` module in place — do not modify it.
2. Load `example_network.json` and print the neighbors of every stop. Confirm you understand the graph before writing any algorithm.
3. Hand-trace `shortest_path("N1", "E2")` on paper. That trace is your first integration test.
4. Build `PriorityQueue` next. Do not touch Dijkstra until its tests are green.
5. Commit early, commit often — expect at least one commit per milestone.
