import os, re
from origami import Origami, point, edge
from fractions import Fraction
import numpy as np


def solve():
    origami = Origami()
    origami.set_default()
    play(origami)
    print(origami.vertices)
    print(origami.edges)

def play(origami = Origami()):
    print(origami.vertices[0], origami.vertices[1])
    origami.fold(origami.vertices[0], origami.vertices[1])


def load():
    print("problem id:")
    problem_id = input()
    path = "./../problems/problem_" + str(problem_id).zfill(5) + ".txt"
    if os.path.exists(path):
        print("id: " + str(problem_id) + " exists.")
    else:
        print("id: " + str(problem_id) + " does not exist.")
        return Origami()
    origami = Origami()
    f = open(path)
    origami.polygon_num = map(int, f.readline().split())[0]
    v_num = map(int, f.readline().split())[0]
    for i in range(v_num):
        v = f.readline().split(',')
        origami.vertices.append(point(Fraction(v[0]), Fraction(v[1])))
    e_num = map(int, f.readline().split())[0]
    for i in range(e_num):
        e = re.split('[, ]', f.readline())
        origami.edges.append([edge(Fraction(e[0]), Fraction(e[1])), edge(Fraction(e[2]), Fraction(e[3]))])
    f.close()
    # print(origami.vertices)
    # print(origami.edges)
    return origami


if __name__ == '__main__':
    solve()
    print("done")