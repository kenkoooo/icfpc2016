# -*- coding: utf-8 -*-
import matplotlib as mp
import os, re
from origami import Origami
from fractions import Fraction

def solve():
	origami = load()


def load():
	print("problem id:")
	problem_id = input()
	path = "./../problems/problem_" + str(problem_id).zfill(5) + ".txt"
	if os.path.exists(path):
		print("id: " + str(problem_id) + " exists.")
	else:
		print("id: " + str(problem_id) + " does not exist.")
		return Origami()
	origami = Origami()
	f = open(path)
	origami.polygon_num = map(int, f.readline().split())[0]
	v_num = map(int, f.readline().split())[0]
	for i in range(v_num):
		v = f.readline().split(',')
		origami.vertices.append([Fraction(v[0]), Fraction(v[1])])
	e_num = map(int, f.readline().split())[0]
	for i in range(e_num):
		e = re.split('[, ]', f.readline())
		origami.edges.append([[Fraction(e[0]), Fraction(e[1])],[Fraction(e[2]), Fraction(e[3])]])
	f.close()
	return origami


if __name__ == '__main__':
	solve()
	print("done")