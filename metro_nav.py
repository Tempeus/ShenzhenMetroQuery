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

    print("Arrived 🎉")

if __name__ == "__main__":
    while True:
        lines = load_lines()
        graph = build_graph(lines)

        start = input("Start station: ")
        end = input("End station: ")

        route = find_route(start, end, lines, graph)

        if route:
            print_route(route)
        else:
            print("No route found")