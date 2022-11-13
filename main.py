import copy
import numpy as np


# реализация переборного алгоритма
def brutforce_algorithm(matrix):
    n = len(matrix)

    # генерируем все возможные варианты расстановки вершинного покрытия
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


# реализация приближённого алгоритма
def approximate_algorithm(main_matrix):
    n = len(main_matrix)
    matrix = copy.deepcopy(main_matrix)

    # вершинное покрытие

    w = []
    viewed = set()

    # зануляем выше главной диагонали
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 0

    # пока в матрице есть рёбра
    # идем по ниже главной диагонали
    while matrix.max() == 1:
        for i in range(n):
            for j in range(0, i):
                # если есть
                if matrix[i][j] == 1:
                    w.append(i + 1)
                    w.append(j + 1)
                    viewed.add(i + 1)
                    viewed.add(j + 1)

                    for s in range(i + 1, n):
                        if matrix[s][i] == 1:
                            viewed.add(s + 1)
                            matrix[s][i] = 0

                    for s in range(j + 1, n):
                        if matrix[s][j] == 1:
                            viewed.add(s + 1)
                            matrix[s][j] = 0

    # если мы не покрыли все вершины, то добавляем их в вершинное покрытие
    if len(viewed) != n:
        temp = set(x for x in range(1, n + 1))
        temp2 = temp.difference(viewed)
        for el in temp2:
            w.append(el)

    return len(w), sorted(w)


def greedy_algorithm():
    # https://pastebin.com/1hNzFYmJ
    print()


# загружаем граф в виде матрицы смежности и возвращаем его
def load_matrix_from_file(file_name):
    # пока для тестов закоментил
    # поменять, чтобы в первой было введено n, но по факту оно не нужно, через len(matrix) потом узнаем n
    # matrix = np.loadtxt(file_name, int, skiprows=1)
    matrix = np.loadtxt(file_name, int)
    return matrix


if __name__ == '__main__':
    input_file_name = "input.txt"

    # удаляет ',' в input файле
    # ',' появляются после сайта graphonline
    with open(input_file_name, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(',', '')
    with open(input_file_name, 'w') as file:
        file.write(filedata)

    matrix = load_matrix_from_file(input_file_name)

    # print(brutforce_algorithm(matrix))
    print(approximate_algorithm(matrix))
