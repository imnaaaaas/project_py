import json
import math 


def generate_network(size: int , filename: str) -> None:
    stops = []
    edges = []
    start_lat=40.70
    start_lon=-74.00
    step=0.01
    stop_number=1

    def distance_between_points(lat1: float , lon1: float , lat2: float ,lon2: float) -> float:# returns distance between two point in kilometrs
        R = 6371 
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        delta_lat=lat2_rad-lat1_rad
        delta_lon=lon2_rad-lon1_rad
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    #stops
    for row in range(size):
        for column in range(size):
            latitude = round(start_lat + row*step,2)
            longitude = round(start_lon + column*step,2)
            stop={
                "id": f"S{stop_number}", #str
                "name": f"Stop {stop_number}", #str
                "lat": latitude, #flotat
                "lon": longitude #float
            }
            stops.append(stop)
            stop_number+=1


    #edges
    for row in range(size):
        for column in range(size):
            current_stop_id = row*size+column+1
            #red line
            if column <size-1:
                right_id = row*size+(column+1)+1

                distance = distance_between_points(
                    stops[current_stop_id-1]["lat"],
                    stops[current_stop_id-1]["lon"],
                    stops[right_id-1]["lat"],
                    stops[right_id-1]["lon"]
                )

                travel_time = round(distance * 2, 2)

                edge = {
                        "from": f"S{current_stop_id}",
                        "to": f"S{right_id}",
                        "travel_time": travel_time,
                        "line_id": "red"
                    }
                edges.append(edge)
                #reverse for a-b b-a
                edge = {
                        "from": f"S{right_id}",
                        "to": f"S{current_stop_id}",
                        "travel_time": travel_time,
                        "line_id": "red"
                    }
                edges.append(edge)

            #blue
            if row <size-1:
                below_id = (row+1)*size+column+1
                distance = distance_between_points(
                    stops[current_stop_id-1]["lat"],
                    stops[current_stop_id-1]["lon"],
                    stops[below_id-1]["lat"],
                    stops[below_id-1]["lon"]
                )

                travel_time = round(distance * 2, 2)
                edge = {
                        "from": f"S{current_stop_id}",
                        "to": f"S{below_id}",
                        "travel_time": travel_time,
                        "line_id": "blue"
                    }
                edges.append(edge)
                edge = {
                        "from": f"S{below_id}",
                        "to": f"S{current_stop_id}",
                        "travel_time": travel_time,
                         "line_id": "blue"
                    }
                edges.append(edge)

        # diagonal down-right (green line)
            if row < size-1 and column < size-1:
            
                diagonal_id = (row+1)*size + (column+1) + 1
                distance = distance_between_points(
                    stops[current_stop_id-1]["lat"],
                    stops[current_stop_id-1]["lon"],
                    stops[diagonal_id-1]["lat"],
                    stops[diagonal_id-1]["lon"]
                )

                travel_time = round(distance * 2, 2)
                edge = {
                    "from": f"S{current_stop_id}",
                    "to": f"S{diagonal_id}",
                    "travel_time": travel_time,
                    "line_id": "green"
                }

                edges.append(edge)


                edge = {
                    "from": f"S{diagonal_id}",
                    "to": f"S{current_stop_id}",
                    "travel_time": travel_time,
                    "line_id": "green"
                }

                edges.append(edge)


    network = {
        "stops":stops,
        "edges":edges
    }

    with open(filename,"w") as f:
        json.dump(network,f,indent=4)


#generate_network(10, "example_network_100.json")
#generate_network(32, "example_network_1000.json")
#generate_network(100, "example_network_10000.json")