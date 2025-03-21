# Сортировка выбором по возрастанию
class SelectionSort:
    @staticmethod
    def get_smallest_num_index(input_list):
        """Находит индекс наименьшего числа в списке input_list"""

        smallest_num = input_list[0]
        smallest_num_index = 0
        for i in range(1, len(input_list)):
            if input_list[i] < smallest_num:
                smallest_num = input_list[i]
                smallest_num_index = i
        return smallest_num_index

    @staticmethod
    def sort(input_list):
        """Сортирует список input_list при помощи алгоритма сортировки выбором"""
        result_list = []
        remaining_list = input_list[:]
        while remaining_list:
            smallest_num = SelectionSort.get_smallest_num_index(remaining_list)
            result_list.append(remaining_list.pop(smallest_num))
        return result_list


# Быстрая сортировка
class QuickSort:
    @staticmethod
    def sort(input_list):
        """Сортирует список input_list при помощи алгоритма быстрой сортировки"""
        remaining_list = input_list[:]
        if len(remaining_list) < 2:
            return remaining_list
        else:
            pivot_index = len(remaining_list) // 2
            pivot = remaining_list[pivot_index]
            remaining_list.pop(pivot_index)
            less = [i for i in remaining_list if i <= pivot]
            greater = [i for i in remaining_list if i > pivot]
            return QuickSort.sort(less) + [pivot] + QuickSort.sort(greater)


# Реверсирование списка
class Reverse:
    @staticmethod
    def reverse_list(input_list):
        """Возвращает список в обратном порядке"""
        return input_list[::-1]
