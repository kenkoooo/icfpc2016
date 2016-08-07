# -*- coding: utf-8 -*-
from fractions import Fraction
import numpy as np


def point(x, y):
    return np.matrix([Fraction(x), Fraction(y)]).T

def edge(px, py):
    return [px, py]

class Origami:
    def __init__(self):
        self.polygon_num = 1 # 1以外には対応しない予定
        self.vertices = [] # 頂点
        self.edges = [] # 辺

    def set_default(self): # 最初の正方形を生成
        self.polygon_num = 1
        v = [point(0, 0), point(1, 0), point(1, 1), point(0, 1)]
        self.vertices = v
        self.edges = [edge(v[0], v[1]), edge(v[1], v[2]), edge(v[2], v[3]), edge(v[3], v[0])]

    def fold(self, pf, pt): # pfがptに移動するように折る
        pa, pb = self.rotate(pf, pt) # 線分
        for (i, v) in enumerate(self.vertices):
            if self.is_movable(pa, pb, v, pf):
                self.vertices[i] = self.line_symmetric(pa, pb, v)

    # 線分 p1 - p2に関して、qに対象な点rの座標を求める.
    def line_symmetric(self, p1, p2, q):
        x1 = p1[0,0]
        y1 = p1[1,0]
        x2 = p2[0,0]
        y2 = p2[1,0]
        xq = q[0,0]
        yq = q[1,0]

        if x1 == x2:
            xr = 2 * x1 - xq
            yr = yq
            return point(xr, yr)

        if y1 == y2:
            xr = xq
            yr = 2 * y1 - yq
            return point(xr, yr)

        a = (y2 - y1) / (x2 - x1)
        b = -1
        c = y2 - x2 * (y2 - y1) / (x2 - x1)
        xr = xq - 2 * a * (a * xq + b * yq + c) / (a ** 2 + b ** 2)
        yr = yq - 2 * b * (a * xq + b * yq + c) / (a ** 2 + b ** 2)

        return point(xr, yr)

    # pfがptに移動するように折る時の折り目の線分を求める
    def rotate(self, pf, pt): # 線分 pf - pt を中点で90度回転
        mid = (pf + pt) / 2
        pf_rot = mid + np.matrix([[0, -1], [1, 0]]) * (pf - mid)
        pt_rot = mid + np.matrix([[0, -1], [1, 0]]) * (pt - mid)
        return pf_rot, pt_rot

    # pa, pbを通る直線ax+by+c=0のa,b,c
    def line(self, pa, pb): #x: [0,0] y: [1,0]
        ax = pa[0,0]
        ay = pa[1,0]
        bx = pb[0,0]
        by = pb[1,0]
        a = ay - by
        b = ax - bx
        c = ax * by - ay * bx
        print("line:", a, b, c)
        return a, b, c

    # 線分pa-pbに対し点p, qが同じ側にあるかどうか判定
    def is_movable(self, pa, pb, p, q):
        a, b, c = self.line(pa, pb)
        px = p[0, 0]
        py = p[1, 0]
        qx = q[0, 0]
        qy = q[1, 0]
        return (a * px + b * py + c) * (a * qx + b * qy + c) > 0


if __name__ == '__main__':
    pass