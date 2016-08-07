import sys

import matplotlib.pyplot as plt

import InputVisualizer

sys.path.append('/Users/um003282/icfpc2016/solver/')
sys.path.append('/Users/um003282/icfpc2016/visualizer/')
sys.path.append('/Users/um003282/icfpc2016/')
import ConvexSolver
from ConvexSolver import PolygonNode
from fractions import Fraction
from sympy.geometry import Point2D

polygon_nodes = [PolygonNode([], False, [
    Point2D(Fraction(0), Fraction(0)),
    Point2D(Fraction(0), Fraction(1)),
    Point2D(Fraction(1), Fraction(0)),
    Point2D(Fraction(1), Fraction(1))
], -1)
                 ]
polygon_nodes[0].set_id(0)

polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(0), Fraction(1, 2)),
    Point2D(Fraction(1), Fraction(1, 2))
], True)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(0), Fraction(1, 4)),
    Point2D(Fraction(1), Fraction(1, 4))
], True)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(0), Fraction(1, 8)),
    Point2D(Fraction(1), Fraction(1, 8))
], True)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(2, 8), Fraction(0)),
    Point2D(Fraction(3, 8), Fraction(1, 8))
], False)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(2, 8), Fraction(3, 8)),
    Point2D(Fraction(3, 8), Fraction(2, 8))
], True)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(0), Fraction(2, 8)),
    Point2D(Fraction(1, 8), Fraction(2, 8))
], True)
polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
    Point2D(Fraction(0), Fraction(2, 8)),
    Point2D(Fraction(1, 8), Fraction(3, 8))
], True)
# polygon_nodes = ConvexSolver.make_origami(polygon_nodes, [
#     Point2D(Fraction(0), Fraction(1, 8)),
#     Point2D(Fraction(1, 8), Fraction(0))
# ], False)

facets, sources = ConvexSolver.rollback_polygon_tree(polygon_nodes)
source_set = set()
facets2d = []
sources2d = []
for source in sources:
    for v in source:
        source_set.add(Point2D(v[0], v[1]))
source_set = list(source_set)
destiny_set = [0] * len(source_set)

output_facets = []
for i in range(len(sources)):
    output_facet = []
    for j in range(len(sources[i])):
        s = sources[i][j]
        p = Point2D(s[0], s[1])
        idx = source_set.index(p)
        destiny_set[idx] = facets[i][j]
        if idx not in output_facet:
            output_facet.append(idx)
    output_facets.append(output_facet)

polygons = []
for facet in output_facets:
    polygon = [destiny_set[i] for i in facet]
    polygons.append(polygon)

# print(len(source_set))
# for v in source_set:
#     print(str(v[0]) + "," + str(v[1]))
# print(len(output_facets))
# for facet in output_facets:
#     print(str(len(facet)) + " " + " ".join(map(str, facet)))
# for v in destiny_set:
#     print(str(v[0]) + "," + str(v[1]))
#
# for facet in output_facets:
#     print([str(destiny_set[i]) for i in facet])

InputVisualizer.plot(polygons, [], [0, 0])
plt.show()
