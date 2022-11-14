import copy
import numpy as np
import random


# реализация переборного алгоритма
def brutforce_algorithm(matrix):
    n = len(matrix)
    smallest_vertex_cover = [1 for i in range(n)]
    # генерируем все возможные варианты расстановки вершинного покрытия
    for number in range(1, 2 ** n):

        # создаём список. конвертируем число int -> binary. слева заполняем нулями до n символов
        # чтобы получилось, например, число вида 0010 и из него список [0, 0, 1, 0]
        vertex_cover_indexes = [int(z) for z in f"{number:b}".zfill(n)]
        viewed_vertices = copy.deepcopy(vertex_cover_indexes)

        # добавляем в "увиденные" смежные вершины
        for i in range(n):
            if vertex_cover_indexes[i] == 1:
                for index, element in enumerate(matrix[i]):
                    if element == 1:
                        viewed_vertices[index] = 1

        # если покрыли все вершины выводим в smallest_vertex_cover при условии
        if sum(viewed_vertices) == n and sum(smallest_vertex_cover) > sum(vertex_cover_indexes):
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
    viewed_vertices = set()

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
                    smallest_vertex_cover.append(i + 1)
                    smallest_vertex_cover.append(j + 1)
                    viewed_vertices.add(i + 1)
                    viewed_vertices.add(j + 1)

                    # добавляем в "увиденные" смежные вершины
                    for s in range(i + 1, n):
                        if matrix[s][i] == 1:
                            viewed_vertices.add(s + 1)
                            matrix[s][i] = 0

                    for s in range(j + 1, n):
                        if matrix[s][j] == 1:
                            viewed_vertices.add(s + 1)
                            matrix[s][j] = 0

    # если мы не покрыли все вершины, то добавляем их в вершинное покрытие
    if len(viewed_vertices) != n:
        set_of_all_vertices = set(x for x in range(1, n + 1))
        set_of_vertices_to_add_to_the_coverage = set_of_all_vertices.difference(viewed_vertices)
        for element in set_of_vertices_to_add_to_the_coverage:
            smallest_vertex_cover.append(element)

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
    viewed_vertices = set()

    n = len(main_matrix)
    matrix = copy.deepcopy(main_matrix)

    degrees_of_vertices = count_degrees_of_vertices(matrix)

    # пока есть ребра или мы не "увидели" все вершины через помеченные покрытыми
    while sum(degrees_of_vertices) != 0 and len(viewed_vertices) != n:
        huge_vertex = degrees_of_vertices.index(max(degrees_of_vertices))
        # добавляем в покрытие
        smallest_vertex_cover.append(huge_vertex + 1)
        viewed_vertices.add(huge_vertex + 1)

        # удаляем ребра инцидентные покрытой вершине
        # также помечая видимые вершины по этим ребрам
        for i in range(n):
            if matrix[i][huge_vertex] == 1:
                viewed_vertices.add(i + 1)

                # случай если граф не связанный
                for q in range(n):
                    if matrix[i][q] == 1 and q + 1 in viewed_vertices and i + 1 in viewed_vertices:
                        matrix[i][q] = 0
                        matrix[q][i] = 0
            matrix[i][huge_vertex] = 0
            matrix[huge_vertex][i] = 0

        degrees_of_vertices = count_degrees_of_vertices(matrix)

    # если мы не покрыли все вершины, то добавляем их в вершинное покрытие
    # например, если граф не связный
    if len(viewed_vertices) != n:
        set_of_all_vertices = set(x for x in range(1, n + 1))
        set_of_vertices_to_add_to_the_coverage = set_of_all_vertices.difference(viewed_vertices)
        for element in set_of_vertices_to_add_to_the_coverage:
            smallest_vertex_cover.append(element)

    return len(smallest_vertex_cover), sorted(smallest_vertex_cover)


# загружаем граф в виде матрицы смежности и возвращаем его
def load_matrix_from_file(file_name):
    matrix = np.loadtxt(file_name, int)
    return matrix


def tests_generator(number_of_graphs, percentage_of_edges):
    for n in range(3, number_of_graphs + 1):
        matrix = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            flag = False
            for j in range(0, i):
                if random.uniform(0, 1) < percentage_of_edges:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
                    flag = True
            if not flag:
                if i != 0:
                    pos = random.randrange(0, i)
                    matrix[i][pos] = 1
                    matrix[pos][i] = 1
        np.savetxt(f'tests/{n}.txt', matrix, fmt='%d', delimiter=' ')
        np.savetxt(f'tests/graphonline/{n}.txt', matrix, fmt='%d', delimiter=', ', newline=', \n')


if __name__ == '__main__':
    input_file_name = "tests/15.txt"

    # удаляет ',' в input файле
    # ',' появляются после сайта graphonline
    with open(input_file_name, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(',', '')
    with open(input_file_name, 'w') as file:
        file.write(filedata)

    matrix = load_matrix_from_file(input_file_name)

    print(brutforce_algorithm(matrix))
    print(approximate_algorithm(matrix))
    print(greedy_algorithm(matrix))

    # tests_generator(15, 0.4)
