import sys
import math
from common.utils import run
from common.grid import grid_from_lines, Cell, Point, Grid
import heapq


START = "S"
END = "E"
WALL = "#"
EMPTY = "."

# orientations
N = "North"
S = "South"
E = "East"
W = "West"


def opposite(dir: str) -> str:
    if dir == N:
        return S
    if dir == S:
        return N
    if dir == E:
        return W
    if dir == W:
        return E


def get_rotation_points(r_from: str, r_to: str) -> int:
    vert = [N, S]
    horz = [E, W]
    if r_from == r_to:
        return 0
    elif (r_from in vert and r_to in vert) or (r_from in horz and r_to in horz):
        return 2000
    else:
        return 1000


def is_junction(cell: Cell, maze: Grid) -> bool:
    neighbours = [neighbour.val for neighbour in maze.get_neighbours(cell.point)]
    return sum([1 if neighbour != WALL else 0 for neighbour in neighbours])


def get_direction(from_point: Point, to_point: Point) -> str:
    if from_point.x == to_point.x and (from_point.y - 1) == to_point.y:
        return N
    elif from_point.x == to_point.x and (from_point.y + 1) == to_point.y:
        return S
    elif (from_point.x + 1) == to_point.x and from_point.y == to_point.y:
        return E
    elif (from_point.x - 1) == to_point.x and from_point.y == to_point.y:
        return W


def to_graph(maze: Grid) -> dict[(Point, str), dict[(Point, str), int]]:
    graph = dict()

    for cell in maze:
        if cell.val != WALL:
            graph[(cell.point, N)] = {(cell.point, E): 1000, (cell.point, W): 1000}
            graph[(cell.point, E)] = {(cell.point, N): 1000, (cell.point, S): 1000}
            graph[(cell.point, S)] = {(cell.point, E): 1000, (cell.point, W): 1000}
            graph[(cell.point, W)] = {(cell.point, S): 1000, (cell.point, N): 1000}
            neighbours = maze.get_neighbours(cell.point)
            for neighbour in neighbours:
                if neighbour.val != WALL:
                    neighbour_dir = get_direction(cell.point, neighbour.point)
                    graph[(cell.point, neighbour_dir)][(neighbour.point, neighbour_dir)] = 1

    return graph


# I can never remember how dijskstra's works
# Code implemented using overview from https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/?ref=lbp
def shortest_distances(
    graph: dict[(Point, str), dict[(Point, str), int]], from_point_dir: (Point, str)
) -> dict[(Point, str), (int, list[(Point, str)])]:
    # Create a set sptSet (shortest path tree set) that keeps track of vertices included in the shortest path tree, i.e., whose minimum distance from the source is calculated and finalized. Initially, this set is empty.
    shortest_path_tree = set()
    all_nodes = set(graph.keys())
    # Assign a distance value to all vertices in the input graph. Initialize all distance values as INFINITE . Assign the distance value as 0 for the source vertex so that it is picked first.
    distances: dict[(Point, str), (int, (Point, str))] = dict()
    for node in all_nodes:
        if node == from_point_dir:
            distances[node] = (0, [])
        else:
            distances[node] = (math.inf, [])

    heap = [(distances[node][0], node) for node in all_nodes]
    heapq.heapify(heap)

    # While sptSet doesn’t include all vertices
    while not shortest_path_tree.issuperset(all_nodes):
        # Pick a vertex u that is not there in sptSet and has a minimum distance value.
        _, min_dist_node = heapq.heappop(heap)
        while min_dist_node in shortest_path_tree and heap:
            _, min_dist_node = heapq.heappop(heap)

        # Include u to sptSet .
        shortest_path_tree.add(min_dist_node)
        min_dist_to_node, _ = distances[min_dist_node]
        # Then update the distance value of all adjacent vertices of u .
        # To update the distance values, iterate through all adjacent vertices.
        for adj_node, adj_node_distance in graph[min_dist_node].items():
            # For every adjacent vertex v, if the sum of the distance value of u (from source) and weight of edge u-v , is less than the distance value of v , then update the distance value of v .
            existing_min_dist, existing_parent_nodes = distances[adj_node]
            maybe_new_min_dist = min_dist_to_node + adj_node_distance
            if maybe_new_min_dist <= existing_min_dist:
                distances[adj_node] = (maybe_new_min_dist, existing_parent_nodes + [min_dist_node])
                heapq.heappush(heap, (maybe_new_min_dist, adj_node))
    return distances


def solution_2024_16_A(filename: str) -> int:
    with open(filename) as lines:
        lines = list(lines)
    maze = grid_from_lines(lines)

    start_point = [cell.point for cell in maze if cell.val == START][0]
    end_point = [cell.point for cell in maze if cell.val == END][0]
    start_dir = E

    graph = to_graph(maze)

    distances = shortest_distances(graph, (start_point, start_dir))

    return min(
        [
            distances[(end_point, N)][0],
            distances[(end_point, S)][0],
            distances[(end_point, E)][0],
            distances[(end_point, W)][0],
        ]
    )


def solution_2024_16_B(filename: str) -> int:
    with open(filename) as lines:
        lines = list(lines)
    maze = grid_from_lines(lines)

    start_point = [cell.point for cell in maze if cell.val == START][0]
    end_point = [cell.point for cell in maze if cell.val == END][0]
    start_dir = E

    graph = to_graph(maze)
    distances = shortest_distances(graph, (start_point, start_dir))

    nodes_on_shortest_paths = set([end_point, start_point])

    shortest_distance, parents = min(
        [
            distances[(end_point, N)],
            distances[(end_point, S)],
            distances[(end_point, E)],
            distances[(end_point, W)],
        ]
    )

    while parents:
        parent = parents.pop()
        nodes_on_shortest_paths.add(parent[0])
        _, next_parents = distances[parent]
        parents = parents + next_parents

    return len(nodes_on_shortest_paths)


def test_solution_2024_16_A():
    assert solution_2024_16_A("./2024_16/test_input.txt") == 11048  # Replace with expected output for the test case
    assert solution_2024_16_A("./2024_16/test_input_2.txt") == 7036


# def test_final_solution_2024_16_A():
#    assert solution_2024_16_A('./2024_16/input.txt') == 0 # Replace with solution when known


def test_solution_2024_16_B():
    assert solution_2024_16_B("./2024_16/test_input_2.txt") == 45
    assert solution_2024_16_B("./2024_16/test_input.txt") == 64  # Replace with expected output for the test case


# def test_final_solution_2024_16_B():
#    assert solution_2024_16_B('./2024_16/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_16", sys.argv[1], solution_2024_16_A, solution_2024_16_B)
