from transit.graph import load_graph_from_json
from transit.router import Router


class Network:
    def __init__(self, json_path):
        self.graph = load_graph_from_json(json_path)
        self.router = Router(self.graph)

    def shortest_path(self, start: str , end: str) -> list[str]:
        return self.router.shortest_path(start, end)

    def shortest_path_astar(self, start: str , end: str) -> list[str]:
        return self.router.shortest_path_astar(start, end)

    def shortest_path_with_transfers(self, start: str , end: str, max_transfers: int) -> list[str]:
        return self.router.shortest_path_with_transfers(start, end, max_transfers)

    def distance_between_points(self, start: str , end: str) -> float:
        return self.router.distance_between_points(start, end)

    def disable_stop(self, stop_id: str) -> None:
        self.graph.disable_stop(stop_id)

    def enable_stop(self, stop_id: str) -> None:
        self.graph.enable_stop(stop_id)

    def disable_edge(self, from_id: str , to_id: str, line_id: str) -> None:
        self.graph.disable_edge(from_id, to_id, line_id)

    def enable_edge(self, from_id: str , to_id: str, line_id: str) -> None:
        self.graph.enable_edge(from_id, to_id, line_id)


    def get_last_visited_nodes(self):
        return self.router.visited_nodes