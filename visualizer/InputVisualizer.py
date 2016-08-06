import argparse
import os
from fractions import Fraction

import matplotlib.pyplot as plt


def plot(polygons, skeleton):
    plt.xlim([-0.5, 1.5])
    plt.ylim([-0.5, 1.5])

    # 縦横比を揃えるおまじない
    plt.gca().set_aspect('equal', adjustable='box')

    # グリッド
    plt.grid(which='major', color='black', linestyle='dashed')

    for polygon in polygons:
        plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))

    for edge in skeleton:
        line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
        plt.gca().add_patch(line)


def pop_input(lines):
    if len(lines) == 0:
        return input()
    return lines.pop(0)


def read_input(lines):
    """
    lines から入力を読みだす。
    lines が空なら標準入力から入力を読みだす。
    多角形とスケルトンのリストにして返す。
    """
    n = int(pop_input(lines))
    polygons = []
    for i in range(n):
        v = int(pop_input(lines))
        coordinates = []
        for j in range(v):
            xy = pop_input(lines).split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])
            coordinates.append([x, y])
        polygons.append(coordinates)

    edge_num = int(pop_input(lines))
    skeleton = []
    for i in range(edge_num):
        e = pop_input(lines).split(" ")
        edge = []
        for xy in e:
            xy = xy.split(",")
            x = Fraction(xy[0])
            y = Fraction(xy[1])
            edge.append([x, y])
        skeleton.append(edge)
    return polygons, skeleton


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
        polygons, skeleton = read_input(lines)
        plot(polygons, skeleton)
        plt.savefig(path)
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="./", help="出力先のディレクトリ")
    parser.add_argument('-i', nargs='*', type=argparse.FileType('r'), required=True, help="入力ファイル")
    run(parser.parse_args())
