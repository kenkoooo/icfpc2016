# -*- coding: utf-8 -*-
import argparse
import json
import os
from fractions import Fraction

import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


def e_format(d):
    """
    指数表記にする
    """
    cnt = 0
    while d > 10:
        cnt += 1
        d /= 10
    d = float(d)
    return "{0:.2f}".format(d) + "e+" + str(cnt)


def is_real_area(polygon):
    points = ConvexHull(polygon).vertices
    n = len(points)
    cnt = 0
    for i in range(n):
        if points[(i + 1) % n] > points[i]:
            cnt += 1
    return cnt > 1


def plot(polygons, skeleton, center):
    if abs(center[0]) < 2 ** 60 and abs(center[1]) < 2 ** 60:
        # オーバーフローしない時は今までどおり
        plt.xlim([center[0] - 1.5, center[0] + 1.5])
        plt.ylim([center[1] - 1.5, center[1] + 1.5])
        center = [0, 0]
    else:
        # オーバーフローするとき
        plt.xlim([- 1.5, 1.5])
        plt.ylim([- 1.5, 1.5])

    # 縦横比を揃えるおまじない
    plt.gca().set_aspect('equal', adjustable='box')

    # グリッド
    plt.grid(which='major', color='black', linestyle='dashed')

    holes = []
    for polygon in polygons:
        polygon = [[p[0] - center[0], p[1] - center[1]] for p in polygon]
        if not is_real_area(polygon):
            holes.append(polygon)
        else:
            plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))

    for polygon in holes:
        plt.gca().add_patch(plt.Polygon(polygon, alpha=1.0, color="w"))

    for edge in skeleton:
        edge = [[p[0] - center[0], p[1] - center[1]] for p in edge]
        line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
        plt.gca().add_patch(line)

    # オーバーフローする時は画像に書く
    if center[0] != 0.0 or center[1] != 0.0:
        s = e_format(center[0]) + ", " + e_format(center[1])
        plt.xlabel(s)

    return center


def read_input(lines):
    """
    lines から入力を読みだす。
    lines が空なら標準入力から入力を読みだす。
    多角形とスケルトンのリストにして返す。
    """
    center_x, center_y = 0, 0

    n = int(lines.pop(0))
    polygons = []
    for i in range(n):
        v = int(lines.pop(0))
        coordinates = []
        for j in range(v):
            xy = lines.pop(0).split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])

            if abs(x) > abs(center_x):
                center_x = x
            if abs(y) > abs(center_y):
                center_y = y

            coordinates.append([x, y])
        polygons.append(coordinates)

    edge_num = int(lines.pop(0))
    skeleton = []
    for i in range(edge_num):
        e = lines.pop(0).split(" ")
        edge = []
        for xy in e:
            xy = xy.split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])

            if abs(x) > abs(center_x):
                center_x = x
            if abs(y) > abs(center_y):
                center_y = y

            edge.append([x, y])
        skeleton.append(edge)
    return polygons, skeleton, [center_x, center_y]


def run(args):
    # 保存先のディレクトリが存在しなければ作成
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    for f in args.i:
        filename = os.path.basename(f.name)
        path = args.o + "/" + filename.replace("txt", "png")
        if os.path.exists(path):
            # 既に画像がある場合は上書きしない
            print(path + " already exists.")
            continue

        print("Loading " + filename + " ...")
        data = f.read()
        lines = data.split("\n")
        polygons, skeleton, center = read_input(lines)
        center = plot(polygons, skeleton, center)
        plt.savefig(path)
        plt.close()

        if center[0] != 0.0 or center[1] != 0.0:
            c = {"x": str(center[0]), "y": str(center[1])}
            f = open(path.replace(".png", "_center.json"), "w")
            json.dump(c, f)
            f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="./", help="出力先のディレクトリ")
    parser.add_argument('-i', nargs='*', type=argparse.FileType('r'), required=True, help="入力ファイル")
    run(parser.parse_args())
