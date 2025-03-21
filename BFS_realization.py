# Реализация поиска в ширину
from algorithms import SearchAlgorithms as s


# Услованая проверка, продает ли человек манго
# Если имя человека оканчивается на 'm', то он продавец манго
def is_mango_seller(name):
    return name[-1] == "m"


# Хеш-таблица показывающая наличие связи между объектами
graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["thom", "jonny"]
graph["anuj"] = []
graph["peggy"] = []
graph["thom"] = []
graph["jonny"] = []

get_mango_seller = s.BFS.search("you", graph, is_mango_seller)
print(get_mango_seller)
