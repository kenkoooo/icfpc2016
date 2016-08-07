# -*- coding: utf-8 -*-

from fractions import Fraction
import numpy as np


class Point:
    def __init__(self, x = Fraction(), y = Fraction(), origin = None):
        self.x = Fraction(x)
        self.y = Fraction(y)
        self.p = np.matrix([x, y]).T

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    @staticmethod
    def point(p):  # np.array形式のものをPointに直す
        return Point(p[0,0], p[1,0])


# 線分vが直線pと交差しているか
def is_crossed(v1 = Point(), v2 = Point(), p1 = Point(), p2 = Point()):
    s1 = (p2.x - p1.x) * (v1.y - p1.y) - (p2.y - p1.y) * (v1.x - p1.x)
    s2 = (p2.x - p1.x) * (v2.y - p1.y) - (p2.y - p1.y) * (v2.x - p1.x)
    if s1 * s2 < 0:
        return True
    else:
        return False


def intersection(p1 = Point(), p2 = Point(), q1 = Point(), q2 = Point()):
    ap = p2.y - p1.y
    bp = p1.x - p2.x
    cp = p1.y * p2.x - p1.x * p2.y
    aq = q2.y - q1.y
    bq = q1.x - q2.x
    cq = q1.y * q2.x - q1.x * q2.y
    d = ap * bq - aq * bp
    x = -bq * cp / d + bp * cq / d
    y = aq * cp / d - ap * cq / d
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

    def cut(self, pf, pt):
        pa, pb = self.rotate(pf, pt)  # 線分
        if not self.is_pierced(pa, pb):
            return [self]
        ind = [-1, -1]  # 貫通した 辺のindex(2つ)
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
                cur ^= 1

        return ret

    # 線分 p1 - p2に関して、qに対象な点rの座標を求める.
    def line_symmetric(self, p1 = Point(), p2 = Point(), q = Point()):
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        xq = q.x
        yq = q.y

        if x1 == x2:
            xr = 2 * x1 - xq
            yr = yq
            return Point(xr, yr)

        if y1 == y2:
            xr = xq
            yr = 2 * y1 - yq
            return Point(xr, yr)

        a = (y2 - y1) / (x2 - x1)
        b = -1
        c = y2 - x2 * (y2 - y1) / (x2 - x1)
        xr = xq - 2 * a * (a * xq + b * yq + c) / (a ** 2 + b ** 2)
        yr = yq - 2 * b * (a * xq + b * yq + c) / (a ** 2 + b ** 2)

        return Point(xr, yr)


    def move_symmetric(self, pf = Point(), pt = Point()): # pfがptに移動するように折る
        pa, pb = self.rotate(pf, pt) # 線分
        # print "pa,pb:", pa.p, pb.p
        for (i, v) in enumerate(self.vertices):
            if self.is_movable(pa, pb, v, pf):
                self.vertices[i] = self.line_symmetric(pa, pb, v)

    def rotate(self, pf =  Point(), pt = Point()): # 線分 pf - pt を中点で90度回転
        mid = (pf.p + pt.p) / 2
        pf_rot = mid + np.matrix([[0, -1], [1, 0]]) * (pf.p - mid)
        pt_rot = mid + np.matrix([[0, -1], [1, 0]]) * (pt.p - mid)
        return Point.point(pf_rot), Point.point(pt_rot)

    # pa, pbを通る直線ax+by+c=0のa,b,c
    def line(self, pa = Point(), pb = Point()):  # x: [0,0] y: [1,0]
        ax = pa.x
        ay = pa.y
        bx = pb.x
        by = pb.y
        a = ay - by
        b = -(ax - bx)
        c = ax * by - ay * bx
        # print("line:", a, b, c)
        return a, b, c


    def is_movable(self, pa = Point(), pb = Point(), p = Point(), q = Point()):
        a, b, c = self.line(pa, pb)
        return (a * p.x + b * p.y + c) * (a * q.x + b * q.y + c) > 0


if __name__ == '__main__':
    polygon = Polygon()
    polygon.default()
    polygon_cut = polygon.cut(Point(Fraction("0"), Fraction("1")), Point(Fraction("-1/5"), Fraction("2/5")))

    print "before folding"
    ka = []
    for i in range(len(polygon_cut)):
        print i, ":"
        for v in polygon_cut[i].vertices:
            print str(v.x), str(v.y)
            ka.append((v.x, v.y))



    for poly in polygon_cut:
        poly.move_symmetric(Point(Fraction("0"), Fraction("1")), Point(Fraction("-1/5"), Fraction("2/5")))

    print "folded"
    kd = {}
    cur = 0
    for i in range(len(polygon_cut)):
        print i, ":"
        for v in polygon_cut[i].vertices:
            print str(v.x), str(v.y)
            kd[(v.x, v.y)] = ka[cur]
            cur += 1

    print kd

    vertex_arr = []
    for i in range(len(polygon_cut)):
        for v in polygon_cut[i].vertices:
            ok = True
            for vt in vertex_arr:
                if vt == v:
                    ok = False
            if ok:
                vertex_arr.append(v)

    print "Begin of Output"
    print len(vertex_arr)
    for v in vertex_arr:
        x, y = kd[(v.x, v.y)]
        print str(x) + "," + str(y)
    print len(polygon_cut)
    for poly in polygon_cut:
        print len(poly.vertices),
        for (i, v) in enumerate(poly.vertices):
            for (j, w) in enumerate(vertex_arr):
                # print v, w
                if v == w:
                    print j,
        print ""


    for i in range(len(vertex_arr)):
        print str(vertex_arr[i].x) + "," + str(vertex_arr[i].y)



