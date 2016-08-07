import argparse
import os
import sys

sys.path.append("./")

from visualizer import InputVisualizer




def run(args):
    for f in args.i:
        filename = os.path.basename(f.name)
        data = f.read()
        lines = data.split("\n")
        polygons, skeleton, center = InputVisualizer.read_input(lines)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", default="./", help="出力先のディレクトリ")
    parser.add_argument('-i', nargs='*', type=argparse.FileType('r'), required=True, help="入力ファイル")
    run(parser.parse_args())
