import argparse
import os
import sys
from fractions import Fraction

import numpy as np
import sympy.geometry as sg
from scipy.spatial import ConvexHull

sys.path.append("./")
from visualizer import InputVisualizer


def get_symmetric_point(p, edge):
    x, y = symmetric_point(
        edge[0][0],
        edge[0][1],
        edge[1][0],
        edge[1][1],
        p[0],
        p[1]
    )
    return [x, y]


class PolygonNode:
    def __init__(self, node_id, edge, is_rotated, vertices, parent_id):
        self.node_id = node_id
        self.edge = edge
        self.is_rotated = is_rotated
        self.vertices = vertices
        self.children_ids = []
        self.parent_id = parent_id

    def has_child(self):
        return len(self.children_ids) > 0

    def split(self, edge, rotate_up):
        """
        :param rotate_up: 線より上の部分が回転するかどうか
        :return:
        """
        line = sg.Line(edge[0], edge[1])
        points = ConvexHull(self.vertices).vertices
        polygon_points = []
        for i in points:
            polygon_points.append(self.vertices[i])
        polygon = sg.Polygon(*polygon_points)
        new_vertices = sg.intersection(polygon, line)


def rotate(a, b, c, p):
    m = np.matrix([
        [Fraction(b, c), -Fraction(a, c)],
        [Fraction(a, c), Fraction(b, c)]
    ])
    v = np.matrix([p])
    v = v.T
    v = m * v
    return [v[0, 0], v[1, 0]]


def is_up(p, edge):
    x1 = edge[0][0]
    y1 = edge[0][1]
    x2 = edge[1][0]
    y2 = edge[1][1]
    a = (y1 - y2) / (x1 - x2)
    k = y1 - a * x1
    return p[1] - (a * p[0] + k)


def is_all_near_up(vs, edge):
    """
    多角形の過半数の点が直線の上にあるかどうか
    :param vs:多角形の頂点たち
    :param edge:直線
    :return:
    """
    up, down = 0, 0
    for p in vs:
        check = is_up(p, edge)
        if check > 0:
            up += 1
        elif check < 0:
            down += 1
    return up > down


def symmetric_point(x1, y1, x2, y2, xq, yq):
    if x1 == x2:
        xr = 2 * x1 - xq
        yr = yq

        return xr, yr

    if y1 == y2:
        xr = xq
        yr = 2 * y1 - yq

        return xr, yr

    a = (y2 - y1) / (x2 - x1)
    b = -1
    c = y2 - x2 * (y2 - y1) / (x2 - x1)

    xr = xq - 2 * a * (a * xq + b * yq + c) / (a ** 2 + b ** 2)
    yr = yq - 2 * b * (a * xq + b * yq + c) / (a ** 2 + b ** 2)

    return xr, yr


def get_symmetric_point(p, edge):
    x, y = symmetric_point(
        edge[0][0],
        edge[0][1],
        edge[1][0],
        edge[1][1],
        p[0],
        p[1]
    )
    return [x, y]


def make_origami(vs, facets, edge, up_flag, lot):
    line = sg.Line(edge)
    broken = []
    for i in range(len(facets)):
        facet = facets[i]
        polygon = sg.Polygon(facet)
        intersections = sg.intersection(line, polygon)
        if len(intersections) == 0:
            continue
        broken.append(i)
        for p in intersections:
            x = p.x
            y = p.y
            vs.append([x, y])


def solve(polygon):
    ids = ConvexHull(polygon).vertices
    x = Fraction(0)
    y = Fraction(0)
    for i in ids:
        x += polygon[i][0]
        y += polygon[i][1]
    x /= len(ids)
    y /= len(ids)
    center = [x / 2, y / 2]

    vs = [
        [Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(1)]
    ]

    facets = [
        [0, 1, 2, 3]
    ]

    for i in range(len(ids)):
        pos = ids[i]
        nex = ids[(i + 1) % len(ids)]
        edge = [polygon[pos], polygon[nex]]
        if is_all_near_up(polygon):
            up = True


def run(args):
    for f in args.i:
        filename = os.path.basename(f.name)
        data = f.read()
        lines = data.split("\n")
        polygons, skeleton, center = InputVisualizer.read_input(lines)
        for polygon in polygons:
            if InputVisualizer.is_real_area(polygon):
                solve(polygon)
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="./", help="出力先のディレクトリ")
    parser.add_argument('-i', nargs='*', type=argparse.FileType('r'), required=True, help="入力ファイル")
    run(parser.parse_args())
