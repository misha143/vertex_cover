import random

import numpy as np


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


tests_generator(22, 0.4)
