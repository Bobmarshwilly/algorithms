"""
Задача 1: Решить каким элементами заполнить рюкзак, так, чтобы забрать как можно больше ценных предметов
Вместимость рюкзака - 6 у.е.
"""

from typing import Any, Dict, Tuple


# Функция решения NP-полной задачи комбинаторной оптимизации
def get_max_value_and_list_of_items(items: Dict[Any, Tuple[int, int]], max_weight: int):
    weight = [i[0] for i in items.values()]
    values = [i[1] for i in items.values()]
    items_count = len(items)
    # Таблица мемоизации
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(items_count + 1)]

    # Заполнение таблицы dp
    for i in range(1, items_count + 1):
        for w in range(1, max_weight + 1):
            if weight[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w], values[i - 1] + dp[i - 1][w - weight[i - 1]]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Оптимальная максимальная ценность объектов, найденная в таблице dp
    max_value = dp[items_count][max_weight]

    # Определение объектов, которые формирует максимальную ценность
    w = max_weight
    items_list = []
    for i in range(items_count, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item_name = list(items.keys())[i - 1]
            items_list.append(item_name)
            w -= weight[i - 1]

    return max_value, items_list


# items - таблица предметов формата item: (weight, value)
# item - название предмета, weight - вес, value - ценность
items = {
    "water": (3, 10),
    "book": (1, 3),
    "food": (2, 9),
    "jacket": (2, 5),
    "camera": (1, 6),
}

max_weight = 6

backpack_max_value, backpack_items_list = get_max_value_and_list_of_items(
    items, max_weight
)
print(
    f"Максимальная ценность рюкзака равна {backpack_max_value}. В рюкзак были положены {backpack_items_list}"
)


"""
Задача 2: Вычислить самую длинную общую подстроку между строками blue и clues
"""
blue = "blue"
clues = "clues"


# Функция нахождение максимальной длины общей подстроки между двумя строками
def get_longest_common_substring(first_str: str, second_str: str):
    len_first_str = len(first_str)
    len_second_str = len(second_str)
    # Таблица мемоизации
    dp = [[0 for _ in range(len_second_str + 1)] for _ in range(len_first_str + 1)]
    max_cell_value = 0  # Максимальная длина общей подстроки

    # Заполнение таблицы dp
    for i in range(1, len_first_str + 1):
        for j in range(1, len_second_str + 1):
            if first_str[i - 1] == second_str[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            # Если значение ячейки больше нынешнего значения переменной, то переменной присваивается значение ячейки
            if dp[i][j] > max_cell_value:
                max_cell_value = dp[i][j]

    return max_cell_value


longest_common_substring = get_longest_common_substring(blue, clues)
print(
    f"Длина самой длинной подстроки между строками {blue} и {clues} состовляет - {longest_common_substring}"
)
