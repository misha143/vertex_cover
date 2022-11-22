import copy
import glob

import numpy as np
import time


# реализация переборного алгоритма
def brutforce_algorithm(matrix):
    if matrix.max() == 0:
        return (0, [])

    n = len(matrix)
    smallest_vertex_cover = [1 for i in range(n)]
    # генерируем все возможные варианты расстановки вершинного покрытия
    for number in range(1, 2 ** n):

        # создаём список. конвертируем число int -> binary. слева заполняем нулями до n символов
        # чтобы получилось, например, число вида 0010 и из него список [0, 0, 1, 0]
        vertex_cover_indexes = [int(z) for z in f"{number:b}".zfill(n)]

        temp_matrix = copy.deepcopy(matrix)
        # удаляем ребра
        for i in range(n):
            if vertex_cover_indexes[i] == 1:
                for index, element in enumerate(temp_matrix[i]):
                    if element == 1:
                        temp_matrix[i][index] = 0
                        temp_matrix[index][i] = 0

        # если покрыли все, то ответный массив обновляем
        if temp_matrix.max() == 0 and sum(smallest_vertex_cover) > sum(vertex_cover_indexes):
            smallest_vertex_cover = vertex_cover_indexes

    indexes_of_covered_vertices = []
    for index, element in enumerate(smallest_vertex_cover):
        if element == 1:
            indexes_of_covered_vertices.append(index + 1)

    return sum(smallest_vertex_cover), indexes_of_covered_vertices


# реализация приближённого алгоритма
def approximate_algorithm(main_matrix):
    n = len(main_matrix)
    matrix = copy.deepcopy(main_matrix)

    # вершинное покрытие
    smallest_vertex_cover = []

    # зануляем выше главной диагонали
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 0

    # пока в матрице есть рёбра
    # идем ниже главной диагонали
    exitFlag = False
    for i in range(n):
        if exitFlag:
            break
        for j in range(0, i):
            # если есть
            if matrix[i][j] == 1:
                smallest_vertex_cover.append(i + 1)
                smallest_vertex_cover.append(j + 1)
                matrix[i][j] = 0

                # удаляем инцидентные ребра
                for s in range(i + 1, n):
                    if matrix[s][i] == 1:
                        matrix[s][i] = 0

                for s in range(j + 1, n):
                    if matrix[s][j] == 1:
                        matrix[s][j] = 0

                for s in range(0, i):
                    if matrix[i][s] == 1:
                        matrix[i][s] = 0

                for s in range(0, j):
                    if matrix[j][s] == 1:
                        matrix[j][s] = 0

                # если ребер нет
                if matrix.max() == 0:
                    exitFlag = True
                    break

    return len(smallest_vertex_cover), sorted(smallest_vertex_cover)


# реализация жадного алгоритма
def greedy_algorithm(main_matrix):
    # подсчёт степеней вершин в графе
    def count_degrees_of_vertices(matrix):
        n = len(matrix)
        degrees_of_vertices = []
        for i in range(n):
            degrees_of_vertices.append(sum(matrix[i]))
        return degrees_of_vertices

    # вершинное покрытие
    smallest_vertex_cover = []

    n = len(main_matrix)
    matrix = copy.deepcopy(main_matrix)

    degrees_of_vertices = count_degrees_of_vertices(matrix)

    # пока есть ребра
    while sum(degrees_of_vertices) != 0:
        huge_vertex = degrees_of_vertices.index(max(degrees_of_vertices))
        # добавляем в покрытие
        smallest_vertex_cover.append(huge_vertex + 1)

        # удаляем ребра инцидентные покрытой вершине
        for i in range(n):
            if matrix[i][huge_vertex] == 1:
                matrix[i][huge_vertex] = 0
                matrix[huge_vertex][i] = 0

        degrees_of_vertices = count_degrees_of_vertices(matrix)

    return len(smallest_vertex_cover), sorted(smallest_vertex_cover)


# загружаем граф в виде матрицы смежности и возвращаем его
def load_matrix_from_file(file_name):
    matrix = np.loadtxt(file_name, int)
    return matrix


if __name__ == '__main__':

    a = int(input(
        "Введите 1 если хотите считать данные из файла\nИначе 2 если хотите запустить на файлах из папки tests\n"))

    if a == 1:

        input_file_name = str(input("Введите путь к файлу. Например: input.txt: "))

        # удаляет ',' в input файле
        # ',' появляются после сайта graph-online
        with open(input_file_name, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(',', '')
        with open(input_file_name, 'w') as file:
            file.write(filedata)

        matrix = load_matrix_from_file(input_file_name)
        with open('results.txt', 'w', encoding='utf-8') as file:
            file.write(f"Минимальное вершинное покрытие. На данных из файла {input_file_name}\n")
            q, w = brutforce_algorithm(matrix)
            file.write(f"Переборный алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n")
            q, w = approximate_algorithm(matrix)
            file.write(f"Приближённый алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n")
            q, w = greedy_algorithm(matrix)
            file.write(f"Жадный алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n\n")
    elif a == 2:
        with open('results.txt', 'w', encoding='utf-8') as file:
            arr = glob.glob(glob.escape(r"tests") + "/*.txt")
            for path in arr:
                matrix = load_matrix_from_file(path)
                file.write(f"Минимальное вершинное покрытие. На данных из файла {path}\n")
                q, w = brutforce_algorithm(matrix)
                file.write(f"Переборный алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n")
                q, w = approximate_algorithm(matrix)
                file.write(f"Приближённый алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n")
                q, w = greedy_algorithm(matrix)
                file.write(f"Жадный алгоритм: кол-во вершин в покрытии {q}, вершины в покрытии: {w}\n\n")

    # s = ""
    # max_time = 120
    # brutforce_algorithm_time = 0
    #
    # file_num = 19
    # loop_cnt1 = 1
    # loop_cnt2 = 50
    # with open('results.txt', 'w') as file:
    #     while (brutforce_algorithm_time < max_time):
    #         input_file_name = f"tests/{file_num}.txt"
    #         matrix = load_matrix_from_file(input_file_name)
    #
    #         s = f"{file_num}\t"
    #
    #         start_time = time.time()
    #         for i in range(loop_cnt1):
    #             a, b = brutforce_algorithm(matrix)
    #         brutforce_algorithm_time = (time.time() - start_time) / loop_cnt1
    #         s += f"{brutforce_algorithm_time}\t{a}\t"
    #
    #         start_time = time.time()
    #         for i in range(loop_cnt2):
    #             a, b = approximate_algorithm(matrix)
    #         s += f"{(time.time() - start_time) / loop_cnt2}\t{a}\t"
    #
    #         start_time = time.time()
    #         for i in range(loop_cnt2):
    #             a, b = greedy_algorithm(matrix)
    #         s += f"{(time.time() - start_time) / loop_cnt2}\t{a}\n"
    #
    #         file.write(s)
    #         file_num += 1
