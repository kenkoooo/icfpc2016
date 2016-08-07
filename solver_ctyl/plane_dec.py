# -*- coding: utf-8 -*-

from fractions import Fraction
import numpy as np
from origami import point, edge

class Point:
    def __init__(self, x = Fraction(), y = Fraction()):
        self.x = Fraction(x)
        self.y = Fraction(y)
        self.p = np.array([x, y]).T

# 線分vが直線pと交差しているか
def is_crossed(v1 = Point(), v2 = Point(), p1 = Point(), p2 = Point()):
    s1 = (p2.x - p1.x) * (v1.y - p1.y) - (p2.y - p1.y) * (v1.x - p1.x)
    s2 = (p2.x - p1.x) * (v2.y - p1.y) - (p2.y - p1.y) * (v2.x - p1.x)
    if s1 * s2 < 0:
        return True
    else:
        return False

def intersection(p1 = Point(), p2 = Point(), q1 = Point(), q2 = Point()):
    ap = p2.y - p1.y;
    bp = p1.x - p2.x;
    cp = p1.y * p2.x - p1.x * p2.y;
    aq = q2.y - q1.y;
    bq = q1.x - q2.x;
    cq = q1.y * q2.x - q1.x * q2.y;
    d = ap * bq - aq * bp;
    x = -bq * cp / d + bp * cq / d;
    y = aq * cp / d - ap * cq / d;
    return Point(x, y)


class Polygon:
    def __init__(self):
        self.vertices = []

    def default(self):
        self.vertices = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)] # 頂点が時計回りに入る

    # 直線(pa-pb)の多角形(self)貫通判定
    def is_pierced(self, pa = Point(), pb = Point()):
        for i in range(len(self.vertices)):
            if is_crossed(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)], pa, pb):
                return True
        return False


    def cut(self, pa, pb):
        if not self.is_pierced(pa, pb):
            return [self]
        ind = [-1, -1] # 貫通した 辺のindex(2つ)
        inter = [Point(), Point()]
        for i in range(len(self.vertices)):
            if is_crossed(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)], pa, pb):
                if ind[0] == -1:
                    ind[0] = i
                    inter[0] = intersection(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)], pa, pb)
                    print inter[0].p
                else:
                    ind[1] = i
                    inter[1] = intersection(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)], pa, pb)
                    print inter[1].p

        ret = [Polygon(), Polygon()]
        cur = 0
        for i in range(len(self.vertices)):
            ret[cur].vertices.append(self.vertices[i])
            if i == ind[cur]:
                ret[cur].vertices.append(inter[cur])
                ret[cur].vertices.append(inter[cur ^ 1])
                cur = cur ^ 1

        return ret

if __name__ == '__main__':
    polygon = Polygon()
    polygon.default()
    polygon_cut = polygon.cut(Point(Fraction("1/2"), 0), Point(Fraction("1/2"), 1))

    print len(polygon_cut)
    for i in range(len(polygon_cut)):
        print i, ":"
        for v in polygon_cut[i].vertices:
            print v.p