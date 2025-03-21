"""
Реализация жадного алгоритма
Задача 1: есть список штатов и таблица радиостанций
Нужно найти такую коомбинацию радиостанций, чтобы покрыть все штаты из списка states_needed'
"""

states_needed = set(["mt", "wa", "or", "id", "nv", "ut", "ca", "az"])

stations = {}
stations["kone"] = set(["id", "nv", "ut"])
stations["ktwo"] = set(["wa", "id", "mt"])
stations["kthree"] = set(["or", "nv", "ca"])
stations["kfour"] = set(["nv", "ut"])
stations["kfive"] = set(["ca", "az"])

final_station = set()
while states_needed:
    best_station = None
    states_covered = set()
    for station, states_for_station in stations.items():
        covered = states_needed & states_for_station
        if len(covered) > len(states_covered):
            best_station = station
            states_covered = covered

    states_needed -= states_covered
    final_station.add(best_station)

print('Решение задачи 1')
print(final_station)


"""
Реализация жадного алгоритма и решение NP-полной задачи
Задача 2: зная расстояние между городами, составить маршрут путешествия по городам с наименьшей длинной общего пути
towns - таблица с значениями расстояний между городами в км
"""
towns = {
    "Nizhny Novgorod": {
        "Moscow": 420,
        "Saint-Petersburg": 927,
        "Voronezh": 439,
        "Kazan": 336,
        "Volgograd": 500,
        "Sochi": 880,
        "Minsk": 1088,
    },
    "Moscow": {
        "Nizhny Novgorod": 420,
        "Saint-Petersburg": 551,
        "Voronezh": 287,
        "Kazan": 752,
        "Volgograd": 646,
        "Sochi": 809,
        "Minsk": 670,
    },
    "Saint-Petersburg": {
        "Nizhny Novgorod": 927,
        "Moscow": 551,
        "Voronezh": 795,
        "Kazan": 1260,
        "Volgograd": 1186,
        "Sochi": 1235,
        "Minsk": 434,
    },
    "Voronezh": {
        "Nizhny Novgorod": 439,
        "Moscow": 287,
        "Saint-Petersburg": 795,
        "Kazan": 703,
        "Volgograd": 398,
        "Sochi": 530,
        "Minsk": 776,
    },
    "Kazan": {
        "Nizhny Novgorod": 336,
        "Moscow": 752,
        "Saint-Petersburg": 1260,
        "Voronezh": 703,
        "Volgograd": 553,
        "Sochi": 1008,
        "Minsk": 1416,
    },
    "Volgograd": {
        "Nizhny Novgorod": 500,
        "Moscow": 646,
        "Saint-Petersburg": 1186,
        "Voronezh": 398,
        "Kazan": 553,
        "Sochi": 459,
        "Minsk": 1161,
    },
    "Sochi": {
        "Nizhny Novgorod": 880,
        "Moscow": 809,
        "Saint-Petersburg": 1235,
        "Voronezh": 530,
        "Kazan": 1008,
        "Volgograd": 459,
        "Minsk": 1044,
    },
    "Minsk": {
        "Nizhny Novgorod": 1088,
        "Moscow": 670,
        "Saint-Petersburg": 434,
        "Voronezh": 776,
        "Kazan": 1416,
        "Volgograd": 1161,
        "Sochi": 1044,
    },
}


route = []  # Маршрут поездки
visited = []  # Посещенные города

first_town = "Minsk"  # Начальный город
route.append(first_town)  # Добавление начального города в маршрутный список route
while len(route) < len(towns):
    town_from = route[-1]
    visited.append(town_from)
    town_to = None
    distance = float("inf")
    for town in towns[town_from].keys():
        if towns[town_from][town] < distance and town not in visited:
            distance = towns[town_from][town]
            town_to = town
    route.append(town_to)

print('Решение задачи 2')
print(*route, sep=" -> ")  # Вывод маршрута
