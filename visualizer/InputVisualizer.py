from fractions import Fraction

import matplotlib.pyplot as plt

# 表示範囲はこのくらいが良さそう
plt.xlim([-0.5, 1.5])
plt.ylim([-0.5, 1.5])

# 縦横比を揃えるおまじない
plt.gca().set_aspect('equal', adjustable='box')

# グリッド
plt.grid(which='major', color='black', linestyle='dashed')


def plot(polygons, skeleton):
    for polygon in polygons:
        plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))

    for edge in skeleton:
        line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
        plt.gca().add_patch(line)
    plt.show()


def read_input():
    """
    標準入力から入力を読みだす。
    多角形とスケルトンのリストにして返す。
    """
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
    return polygons, skeleton


def run():
    polygons, skeleton = read_input()
    plot(polygons, skeleton)


if __name__ == '__main__':
    run()
