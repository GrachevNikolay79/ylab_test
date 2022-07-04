""" salesman - коммивояжёр. Алгоритм построения кратчайшего пути обхода всех точек.
Пример использования:
        import random as rd

        import datetime as dt

        p = [(rd.randint(0, 50), rd.randint(0, 50)) for _ in range(15)]

        t1 = dt.datetime.now()

        salesman(p)

        t2 = dt.datetime.now()

        print("Elapsed time:{}".format(t2-t1))
"""
import math

MAX_SIZE = float('inf')
final_path = []  # Хранит окончательное решение т.е. путь продавца.
final_res = 0.0  # Хранит окончательный минимальный вес кратчайшего тура.
mx_size = 0


def copy_to_final(curr_path):
    final_path[:mx_size + 1] = curr_path[:]
    final_path[mx_size] = curr_path[0]


def first_min(matrix, i):
    l_min = MAX_SIZE
    for k in range(mx_size):
        if matrix[i][k] < l_min and i != k:
            l_min = matrix[i][k]
    return l_min


def second_min(matrix, i):
    first, second = MAX_SIZE, MAX_SIZE
    for j in range(mx_size):
        if i == j:
            continue
        if matrix[i][j] <= first:
            second = first
            first = matrix[i][j]
        elif (matrix[i][j] <= second and
              matrix[i][j] != first):
            second = matrix[i][j]
    return second


def walk(matrix, curr_bound, curr_weight, level, curr_path, visited):
    global final_res
    if level == mx_size:
        if matrix[curr_path[level - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + matrix[curr_path[level - 1]][curr_path[0]]
            if curr_res < final_res:
                copy_to_final(curr_path)
                final_res = curr_res
        return
    for i in range(mx_size):
        if matrix[curr_path[level - 1]][i] != 0 and not visited[i]:
            temp = curr_bound
            curr_weight += matrix[curr_path[level - 1]][i]
            if level == 1:
                curr_bound -= ((first_min(matrix, curr_path[level - 1]) + first_min(matrix, i)) / 2)
            else:
                curr_bound -= ((second_min(matrix, curr_path[level - 1]) + first_min(matrix, i)) / 2)
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True
                walk(matrix, curr_bound, curr_weight, level + 1, curr_path, visited)
            curr_weight -= matrix[curr_path[level - 1]][i]
            curr_bound = temp

            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def get_len(p1: list, p2: list) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def salesman(points: list):
    """ points = [[0, 0], [3, 7], ... [43, 12]]  - список координат точек.

        points[0] - точка старта, она же финиш.
        Но, по идее, без разницы, т.к. маршрут закольцован
    """

    global final_path
    global final_res
    global mx_size
    matrix = [[get_len(i, j) for i in points] for j in points]
    mx_size = len(matrix)
    final_path = [0] * (mx_size + 1)
    final_res = MAX_SIZE

    curr_bound = 0
    curr_path = [-1] * (mx_size + 1)
    visited = [False] * mx_size
    for i in range(mx_size):
        curr_bound += (first_min(matrix, i) + second_min(matrix, i))
    curr_bound = math.ceil(curr_bound / 2)
    visited[0] = True
    curr_path[0] = 0

    walk(matrix, curr_bound, 0, 1, curr_path, visited)

    v = 0
    for i in range(mx_size + 1):
        fpi = final_path[i]
        if i == 0:
            print(points[fpi], end=' ')
        else:
            v += matrix[final_path[i - 1]][fpi]
            print("-> {}{}".format(points[fpi], v), end=' ')
    print("= {}".format(final_res))
