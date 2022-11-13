import copy

import numpy as np


# реализация переборного алгоритма
def brutforce_algorithm(matrix):
    n = len(matrix)

    temp_ans_arr = []
    ans_cnt = n + 1

    # генерируем все возомжные варианты расстановки "камер"
    for q in range(1, 2 ** n):

        # создаём список. конвертируем число int -> binary. слева заполняем нулями до n символов
        binary_array = [int(z) for z in f"{q:b}".zfill(n)]
        temp = copy.deepcopy(binary_array)

        # закрашиваем вершины, которые мы видим из ранее заданных вершин с "камерами"
        for i in range(n):
            if binary_array[i] == 1:
                for index, el in enumerate(matrix[i]):
                    if el == 1:
                        temp[index] = 1

        # если покрыли все вершины и кол-во "камер" меньше чем в прошлые разы, то заполняем в ответы
        if sum(temp) == n and sum(binary_array) < ans_cnt:
            ans_cnt = sum(binary_array)
            temp_ans_arr = binary_array

    # заполняем ответный массив вершин
    ans_arr = []
    for index, el in enumerate(temp_ans_arr):
        if el == 1:
            ans_arr.append(index + 1)
    return ans_cnt, ans_arr


# загружаем граф в виде матрицы смежности и возвращаем его
def load_matrix_from_file(file_name):
    # пока для тестов закоментил
    # поменять, чтобы в первой было введено n, но по факты оно не нужно, через len(matrix) потом узнаем n
    # matrix = np.loadtxt(file_name, int, skiprows=1)
    matrix = np.loadtxt(file_name, int)
    return matrix


if __name__ == '__main__':
    input_file_name = "input.txt"
    matrix = load_matrix_from_file(input_file_name)
    print(brutforce_algorithm(matrix))
