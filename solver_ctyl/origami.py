# -*- coding: utf-8 -*-
from fractions import Fraction


def point(self, x, y):
    return [Fraction(x), Fraction(y)]
def edge(self, px, py):
    return [px, py]

class Origami:
    def __init__(self):
        self.polygon_num = 1
        self.vertices = []
        self.edges = []

    def set_default(self):
        self.polygon_num = 1
        v = [point(0, 0), point(1, 0), point(1, 1), point(0, 1)]
        self.vertices = v
        self.edges = [edge(v[0], v[1]), edge(v[1], v[2]), edge(v[2], v[3]), edge(v[3], v[0])]

    def fold(self, pf, pt): # pfがptに移動するように折る
        pass







if __name__ == '__main__':
    pass