from algorithms import SortingAlgorithms as s
from random import *


lst = [randint(0, 10) for i in range(10)]
print(f"Оригинальный список: {lst}")
selection_sort_lst = s.SelectionSort.sort(lst)
print(f"Отсортированный список при помощи соритровки выбором: {selection_sort_lst}")

lst2 = [randint(0, 10) for i in range(10)]
print(f"Оригинальный список: {lst2}")
quick_sorting_lst = s.QuickSort.sort(lst2)
print(f"Отсортированный список при помощи быстрой сортировки: {quick_sorting_lst}")
