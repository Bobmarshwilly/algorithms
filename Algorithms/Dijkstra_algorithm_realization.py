# Реализация алгоритма Дейкстры
graph = {}
graph["start"] = {}
graph["start"]["a"] = 5
graph["start"]["b"] = 2
graph["a"] = {}
graph["a"]["c"] = 4
graph["a"]["d"] = 2
graph["b"] = {}
graph["b"]["a"] = 8
graph["b"]["d"] = 7
graph["c"] = {}
graph["c"]["d"] = 6
graph["c"]["final"] = 3
graph["d"] = {}
graph["d"]["final"] = 1
graph["final"] = {}

infinity = 10**9
costs = {}
costs["a"] = 5
costs["b"] = 2
costs["c"] = infinity
costs["d"] = infinity
costs["final"] = infinity

parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["c"] = None
parents["d"] = None
parents["final"] = None


from algorithms import SearchAlgorithms as s


shortest_way = s.Dijkstra.search("start", "final", graph, costs, parents)
print(
    f"Кратчайший путь из start в final: {shortest_way}.\n"
    f"Длина маршрута состовляет - {costs['final']}"
)
