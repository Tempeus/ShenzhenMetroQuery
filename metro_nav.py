from collections import defaultdict, deque
import os

LINES_FOLDER = "./lines"

def load_lines():
    lines = {}
    for filename in os.listdir(LINES_FOLDER):
        if filename.endswith(".txt"):
            with open(os.path.join(LINES_FOLDER, filename), encoding="utf-8") as f:
                stations = [line.strip() for line in f if line.strip()]
                lines[filename.replace(".txt", "")] = stations
    return lines

def build_graph(lines):
    graph = defaultdict(list)
    station_lines = defaultdict(list)

    # Track which stations are on which lines
    for line, stations in lines.items():
        for s in stations:
            station_lines[s].append(line)

    # Connect adjacent stations on same line
    for line, stations in lines.items():
        for i, station in enumerate(stations):
            if i > 0:
                graph[(station, line)].append((stations[i-1], line))
            if i < len(stations) - 1:
                graph[(station, line)].append((stations[i+1], line))

    # Add transfer edges
    for station, lines_here in station_lines.items():
        if len(lines_here) > 1:
            for line in lines_here:
                for other_line in lines_here:
                    if line != other_line:
                        graph[(station, line)].append((station, other_line))

    return graph

def find_route(start, end, lines, graph):
    queue = deque()
    visited = set()

    # You can start on any line that contains the start station
    for line in lines:
        if start in lines[line]:
            queue.append(((start, line), [(start, line)]))
            visited.add((start, line))

    while queue:
        (station, line), path = queue.popleft()

        if station == end:
            return path

        for next_station, next_line in graph[(station, line)]:
            state = (next_station, next_line)
            if state not in visited:
                visited.add(state)
                queue.append((state, path + [state]))

    return None

def print_route(route):
    current_line = route[0][1]
    print(f"Start on {current_line}")

    for i in range(1, len(route)):
        station, line = route[i]
        prev_station, prev_line = route[i - 1]

        if line != prev_line:
            print(f"Transfer at {station} to {line}")
        else:
            print(f"  → {station}")

    print("Arrived 🎉\n\n")

def get_station_to_lines(lines):
    station_to_lines = defaultdict(set)
    for line, stations in lines.items():
        for station in stations:
            station_to_lines[station].add(line)
    return station_to_lines

def get_metro_info(line_name, lines):
    if line_name not in lines:
        return None

    stations = lines[line_name]
    station_to_lines = get_station_to_lines(lines)

    transfers = {}
    for station in stations:
        connected_lines = station_to_lines[station] - {line_name}
        if connected_lines:
            transfers[station] = list(connected_lines)

    info = {
        "line": line_name,
        "station_count": len(stations),
        "start_station": stations[0],
        "end_station": stations[-1],
        "stations": stations,
        "transfers": transfers
    }

    return info

def print_metro_info(info):
    print(f"\n🚇 {info['line']}")
    print(f"Stations: {info['station_count']}")
    print(f"From {info['start_station']} → {info['end_station']}")

    if info["transfers"]:
        print("\n🔁 Transfer stations:")
        for station, lines in info["transfers"].items():
            print(f"  • {station} → {', '.join(lines)}")
    else:
        print("\nNo transfer stations")

    print("\n📍 Station list:")
    for s in info["stations"]:
        print(f"  - {s}")   

def get_station_info(station_name, lines):
    station_name = station_name.strip()
    info = {
        "station": station_name,
        "lines": [],
        "is_transfer": False,
        "connections": {}
    }

    for line, stations in lines.items():
        if station_name in stations:
            idx = stations.index(station_name)
            info["lines"].append(line)

            prev_station = stations[idx - 1] if idx > 0 else None
            next_station = stations[idx + 1] if idx < len(stations) - 1 else None

            info["connections"][line] = {
                "previous": prev_station,
                "next": next_station
            }

    info["is_transfer"] = len(info["lines"]) > 1
    return info if info["lines"] else None

def print_station_info(info):
    print(f"\n🚉 Station: {info['station']}")
    print(f"Lines: {', '.join(info['lines'])}")

    if info["is_transfer"]:
        print("Transfer station: YES 🔁")
    else:
        print("Transfer station: NO")

    print("\nConnections:")
    for line, conn in info["connections"].items():
        prev_s = conn["previous"] or "End of line"
        next_s = conn["next"] or "End of line"
        print(f"  {line}: {prev_s} ← {info['station']} → {next_s}")


if __name__ == "__main__":
    lines = load_lines()

    while True:
        answer = input("What you want? \n 1 - Search lines \n 2 - Search Station\n 3 - Pathing\n\n")
        if answer == '1':
            line_name = input("Enter metro line name: ")
            info = get_metro_info(line_name, lines)

            if info:
                print_metro_info(info)
            else:
                print("Line not found")

        elif answer == '2':
            station = input("Enter station name: ")
            info = get_station_info(station, lines)

            if info:
                print_station_info(info)
                print("\n\n")
            else:
                print("Station not found")
                print("\n\n")

        elif answer == '3':
            graph = build_graph(lines)

            start = input("Start station: ")
            end = input("End station: ")

            route = find_route(start, end, lines, graph)

            if route:
                print_route(route)
            else:
                print("No route found")
        else:
            continue