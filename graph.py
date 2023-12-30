from queue import PriorityQueue
import heapq


def Prim(graph):
    current = 1
    size = len(graph)
    checker = [False] * (size + 1)
    pq = []
    checker[current] = True
    selected_edges = []

    for next, w in graph[current]:
        heapq.heappush(pq, (w, current, next))

    tot = 0
    while pq:
        w, from_node, to_node = heapq.heappop(pq)
        if checker[to_node]:
            continue
        tot += w
        checker[to_node] = True
        selected_edges.append((from_node, to_node, w))

        for next, w in graph[to_node]:
            if not checker[next]:
                heapq.heappush(pq, (w, to_node, next))

    return selected_edges, tot
# 그래프는 각 간선별로 (노드 번호, 가중치)로 저장된 형태


def Kruskal(graph):
    edges = []
    size = len(graph)
    parent = [i for i in range(size+1)]

    def find(x):
        if parent[x] == x:
            return x
        else:
            parent[x] = find(parent[x])
            return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)

        if root_x == root_y:
            return
        parent[root_x] = root_y
    for i in range(size):
        for B, W in graph[i]:
            edges.append((W, i, B))
    tot = 0
    mst = []
    total_weight = 0

    for W, A, B in edges:
        if find(A) != find(B):
            union(A, B)
            mst.append((A, B, W))
            total_weight += W

    return mst, total_weight


def dijkstra(graph, size, start, end):
    min_distances = [float('inf')] * (size + 1)
    min_distances[start] = 0

    visited = [False] * (size + 1)

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        current_distance, current_node = pq.get()
        if current_node == end:
            break
        if visited[current_node]:
            continue

        visited[current_node] = True

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < min_distances[neighbor]:
                min_distances[neighbor] = distance
                pq.put((distance, neighbor))

    if float('inf') in min_distances[1:]:
        return float('inf')

    return sum(min_distances) - min_distances[start]


def dijkstra_for_tile_map(tile_map, start, end):
    rows, cols = len(tile_map), len(tile_map[0])
    min_distances = [[float('inf')] * cols for _ in range(rows)]
    start_x, start_y = start
    end_x, end_y = end
    min_distances[start_x][start_y] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    path = []

    while not pq.empty():
        current_distance, (x, y) = pq.get()

        path.append((x, y))

        if (x, y) == end:
            return current_distance, path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and tile_map[nx][ny] == 0:
                new_distance = current_distance + 1
                if new_distance < min_distances[nx][ny]:
                    min_distances[nx][ny] = new_distance
                    pq.put((new_distance, (nx, ny)))

    return float('inf'), path if min_distances[end_x][end_y] == float('inf') else min_distances[end_x][end_y]


def manhattan_distance(node, end):
    x1, y1 = node
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_for_tile_map(tile_map, start, end, heuristic=manhattan_distance):
    rows, cols = len(tile_map), len(tile_map[0])
    min_distances = [[float('inf')] * cols for _ in range(rows)]
    start_x, start_y = start
    end_x, end_y = end
    min_distances[start_x][start_y] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    path = {}
    path[start] = None

    while not pq.empty():
        current_distance, current_node = pq.get()
        x, y = current_node

        if current_node == end:
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and tile_map[nx][ny] == 0:
                new_distance = current_distance + 1 + heuristic((nx, ny), end)
                if new_distance < min_distances[nx][ny]:
                    min_distances[nx][ny] = new_distance
                    pq.put((new_distance, (nx, ny)))
                    path[(nx, ny)] = (x, y)

    return min_distances[end_x][end_y], _reconstruct_path(path, start, end)


def _reconstruct_path(path, start, end):
    if end not in path:
        return []
    current = end
    path_to_return = []
    while current != start:
        path_to_return.append(current)
        current = path[current]
    path_to_return.append(start)
    path_to_return.reverse()
    return path_to_return


if __name__ == "__main__":
    tile_map = [
        [0, -1, 0, 0, 0],
        [0, -1, 0, -1, 0],
        [0, 0, 0, -1, 0],
        [-1, -1, 0, -1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    end = (4, 4)
    distance, path = dijkstra_for_tile_map(tile_map, start, end)
    print("Distance:", distance)
    print("Path:", path)
