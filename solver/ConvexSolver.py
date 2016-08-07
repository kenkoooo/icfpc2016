import argparse
import os
import sys
from fractions import Fraction

import numpy as np
import sympy.geometry as sg
from scipy.spatial import ConvexHull
from sympy.geometry.line import Segment

from symmetric_point import symmetric_point

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


def is_up(p, edge):
    x1 = edge[0][0]
    y1 = edge[0][1]
    x2 = edge[1][0]
    y2 = edge[1][1]
    a = (y1 - y2) / (x1 - x2)
    k = y1 - a * x1
    return p[1] - (a * p[0] + k)


class PolygonNode:
    def __init__(self, edge, is_rotated, vertices, parent_id):
        self.edge = edge
        self.is_rotated = is_rotated
        self.vertices = vertices
        self.children_ids = []
        self.parent_id = parent_id
        self.node_id = -1

    def has_child(self):
        return len(self.children_ids) > 0

    def set_id(self, node_id):
        self.node_id = node_id

    def split(self, edge, rotate_up):
        """
        :param edge:
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

        up = []
        down = []
        on_line = 0
        for v in self.vertices:
            check = is_up(v, edge)
            if check > 0:
                up.append(v)
            else:
                if check == 0:
                    on_line += 1
                down.append(v)
        if on_line == len(down):
            return None, None
        nv_cnt = 0
        for nv in new_vertices:
            if type(nv) == Segment:
                continue
            up.append(nv)
            down.append(nv)
            nv_cnt += 1
        if nv_cnt != 2:
            return None, None

        if rotate_up:
            up = [get_symmetric_point(p, edge) for p in up]
        else:
            down = [get_symmetric_point(p, edge) for p in down]

        up_polygon = PolygonNode(edge, rotate_up, up, self.node_id)
        down_polygon = PolygonNode(edge, not rotate_up, down, self.node_id)

        # GC
        self.vertices = []

        return up_polygon, down_polygon

    def add_child(self, child_id):
        self.children_ids.append(child_id)

    def get_id(self):
        return self.node_id

    def get_parent_id(self):
        return self.parent_id


def rotate(a, b, c, p):
    m = np.matrix([
        [Fraction(b, c), -Fraction(a, c)],
        [Fraction(a, c), Fraction(b, c)]
    ])
    v = np.matrix([p])
    v = v.T
    v = m * v
    return [v[0, 0], v[1, 0]]


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


def make_origami(polygon_nodes, edge, rotate_up):
    """
    polygon_nodes の中の PolygonNode のうち、線と衝突するものを折る。
    線の上側を折り返すときは rotate_up を True にする。
    :param polygon_nodes:
    :param edge:
    :param rotate_up:
    :return:
    """
    size = len(polygon_nodes)
    for parent_id in range(size):
        if polygon_nodes[parent_id].has_child():
            continue
        poly1, poly2 = polygon_nodes[parent_id].split(edge, rotate_up)
        if not poly1:
            continue

        poly1.set_id(len(polygon_nodes))
        polygon_nodes.append(poly1)

        poly2.set_id(len(polygon_nodes))
        polygon_nodes.append(poly2)

        polygon_nodes[parent_id].add_child(poly1.get_id())
        polygon_nodes[parent_id].add_child(poly2.get_id())
    return polygon_nodes


def rollback_polygon_tree(polygon_nodes):
    facets = []
    sources = []
    for polygon_node in polygon_nodes:
        if polygon_node.has_child():
            continue
        node_id = polygon_node.get_id()
        vertices = polygon_node.vertices
        destiny = [v for v in vertices]
        while node_id > 0:
            p = polygon_nodes[node_id]
            edge = p.edge
            if p.is_rotated:
                vertices = [get_symmetric_point(v, edge) for v in vertices]
            node_id = p.parent_id
        facets.append(destiny)
        sources.append(vertices)
    return facets, sources


def solve(polygon):
    ids = ConvexHull(polygon).vertices
    x = Fraction(0)
    y = Fraction(0)
    for i in ids:
        x += polygon[i][0]
        y += polygon[i][1]
    x /= len(ids)
    y /= len(ids)
    x /= 2
    y /= 2

    polygon_nodes = [PolygonNode([], False, [
        [x - Fraction(1, 2), y - Fraction(1, 2)],
        [x - Fraction(1, 2), y + Fraction(1, 2)],
        [x + Fraction(1, 2), y - Fraction(1, 2)],
        [x + Fraction(1, 2), y + Fraction(1, 2)]
    ], -1)]
    polygon_nodes[0].set_id(0)

    for i in range(len(ids)):
        pos = ids[i]
        nex = ids[(i + 1) % len(ids)]
        edge = [polygon[pos], polygon[nex]]
        if is_all_near_up(polygon, edge):
            rotate_up = False
        else:
            rotate_up = True
        polygon_nodes = make_origami(polygon_nodes, edge, rotate_up)


def run(args):
    for f in args.i:
        filename = os.path.basename(f.name)
        data = f.read()
        lines = data.split("\n")
        polygons, skeleton, center = InputVisualizer.read_input(lines)
        for polygon in polygons:
            if InputVisualizer.is_real_area(polygon):
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="./", help="出力先のディレクトリ")
    parser.add_argument('-i', nargs='*', type=argparse.FileType('r'), required=True, help="入力ファイル")
    run(parser.parse_args())
