from fractions import Fraction

import matplotlib.pyplot as plt

# 表示範囲はこのくらいが良さそう
plt.xlim([-0.2, 1.2])
plt.ylim([-0.2, 1.2])


def plot(polygons, skeleton):
    for polygon in polygons:
        plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))

    for edge in skeleton:
        line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
        plt.gca().add_patch(line)

    plt.show()


def run():
    n = int(input())
    polygons = []
    for i in range(n):
        v = int(input())
        coordinates = []
        for j in range(v):
            xy = input().split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])
            coordinates.append([x, y])
        polygons.append(coordinates)

    edge_num = int(input())
    skeleton = []
    for i in range(edge_num):
        e = input().split(" ")
        edge = []
        for xy in e:
            xy = xy.split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])
            edge.append([x, y])
        skeleton.append(edge)
    plot(polygons, skeleton)


if __name__ == '__main__':
    run()
