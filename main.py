import copy
import numpy as np


# реализация переборного алгоритма
def brutforce_algorithm(matrix):
    n = len(matrix)

    # генерируем все возомжные варианты расстановки "камер"
    for q in range(1, 2 ** n):

        # создаём список. конвертируем число int -> binary. слева заполняем нулями до n символов
        # чтобы получилось, например, число вида 0010 и из него список [0, 0, 1, 0]
        binary_array = [int(z) for z in f"{q:b}".zfill(n)]
        temp = copy.deepcopy(binary_array)

        # помечаем вершины которые попали в вершинное покрытие
        for i in range(n):
            if binary_array[i] == 1:
                for index, el in enumerate(matrix[i]):
                    if el == 1:
                        temp[index] = 1

        # если покрыли все вершины выводим ответы
        if sum(temp) == n:
            indexes_of_covered_vertices = []
            for index, el in enumerate(binary_array):
                if el == 1:
                    indexes_of_covered_vertices.append(index + 1)

            return sum(binary_array), indexes_of_covered_vertices


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
