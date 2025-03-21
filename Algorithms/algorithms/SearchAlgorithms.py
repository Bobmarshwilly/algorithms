from collections import deque


class LinearSearch:
    @staticmethod
    def linear_search(lst, item):
        """
        Находит переменную item в списке lst при помощи перебора всез элементов списка

        lst - список элементов
        item - элемент, который необходимо найти в списке lst
        """
        for i in range(len(lst)):
            if lst[i] == item:
                return lst[i]
        return None


# Бинарный поиск переменной item в списке lst
class BinarySearch:
    @staticmethod
    def search(lst, item):
        """
        Находит переменную item в списке lst при помощи бинарного поиска

        lst - отсортированный список элементов
        item - элемент, который необходимо найти в списке lst
        """
        if lst == []:
            return None
        elif len(lst) == 1:
            return lst[0] if lst[0] == item else None
        else:
            get_middle_index = len(lst) // 2  # поиск индекса среднего элемента списка
            get_middle_num = lst[
                get_middle_index
            ]  # определение значения среднего элемента списка
            if item == get_middle_num:
                return get_middle_num
            elif item < get_middle_num:
                return BinarySearch.search(lst[:get_middle_index], item)
            else:
                return BinarySearch.search(lst[get_middle_index + 1 :], item)


# Поиск в ширину
class BFS:
    @staticmethod
    def search(start_item, graph, is_solution):
        """
        Находит такого соседа среди элементов графа, чтобы он удовлетворял входное условие

        start_item - начальный узел, от которого будет производиться поиск
        graph - хеш-таблица связей между элементами(вершинами графа)
        is_solution - функция проверяющая удовлетворение условий поиска
        """
        # Инициализация очереди для хранения узлов на поиск
        search_queue = deque(graph[start_item])
        searched = []  # Проверенные элементы
        while search_queue:
            current_item = search_queue.popleft()  # Извлечение первого узла из очереди
            if current_item not in searched:
                if is_solution(current_item):
                    return current_item  # Если решение найдено, то вернуть его
                else:
                    search_queue.extend(
                        graph[current_item]
                    )  # Добавление соседних узлов current_item
                    searched.append(
                        current_item
                    )  # Добавление current_item в список проверенных
        return None


# Алгоритм Дейкстры
class Dijkstra:
    @staticmethod
    def search(start_node, end_node, graph, costs, parents):
        """
        Находит кратчайший путь от start_node до end_node в графе с использованием алгоритма Дейкстры.

        start_node: Начальный узел
        end_node: Конечный узел
        graph: Хеш-таблица связей между узлами графа
        costs: Таблица стоимости для узлов
        parents: Таблица для отслеживания родителей узлов
        """
        processed = []

        # Поиск узла с наименьшей стоимостью среди необработанных
        def get_lowest_cost_node(costs):
            lowest_cost = 10**9
            lowest_cost_node = None
            for node in costs:
                cost = costs[node]
                if cost < lowest_cost and node not in processed:
                    lowest_cost = cost
                    lowest_cost_node = node
            return lowest_cost_node

        node = get_lowest_cost_node(costs)
        while node is not None:
            cost = costs[node]
            neighbors = graph[node]
            for i in neighbors.keys():
                new_cost = (
                    cost + neighbors[i]  # определение новой стоимости соседнего узла
                )
                if costs[i] > new_cost:
                    costs[i] = (
                        new_cost  # если новая стоимость узла меньше прежней, стоимость узла обновляется
                    )
                    parents[i] = node
            processed.append(node)  # обновление списка обработанных узлов
            node = get_lowest_cost_node(costs)

        return Dijkstra.reconstruct_path(start_node, end_node, parents)

    @staticmethod
    def reconstruct_path(start_node, end_node, parents):
        """
        Восстанавливает кратчайший путь от start_node до end_node.

        start_node: Начальный узел
        end_node: Конечный узел
        parents: Таблица для отслеживания родителей узлов
        return: Кратчайший путь от start_node до end_node в виде списка узлов
        """

        path = []
        current_node = end_node

        while current_node != start_node:
            path.insert(0, current_node)
            current_node = parents[current_node]

        path.insert(0, start_node)
        return path
