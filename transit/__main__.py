# CLI SKELETON
from transit.network import Network
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", default="network_jsons/example_network.json")#json load
    subparsers = parser.add_subparsers(dest="command")
    route_parser = subparsers.add_parser("route")
    route_parser.add_argument("start")
    route_parser.add_argument("end")
    args = parser.parse_args()

    network = Network(args.network)

    if args.command == "route":
        path = network.shortest_path_astar(args.start, args.end)
        print(path)

if __name__ == "__main__":
    main()

#python3 -m transit route N1 E2


#python3 -m transit --network network_jsons/example_network_100.json route S1 S78


"""for max transfers
    network = Network("example_network_100.json")
    print(network.shortest_path_with_transfers("S1", "S20", max_transfers=0))
    print(network.shortest_path_with_transfers("S1", "S20", max_transfers=1))
    print(network.shortest_path_with_transfers("S1", "S20", max_transfers=20))
"""
