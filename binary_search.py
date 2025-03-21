from algorithms import SearchAlgorithms as s

lst = [i for i in range(1000)]  # отсортированный список

binary_search_result = s.BinarySearch.search(lst, 49)  # Поиск числа 49 в списке lst
print(binary_search_result)
