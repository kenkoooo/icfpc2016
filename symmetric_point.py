from fractions import Fraction

"""
線分 P1(x1, y1) - P2(x2, y2)
に関して、点Q(xq, yq)に対象な点R(xr, yr)の座標を求める.
"""

def symmetric_point(x1, y1, x2, y2, xq, yq):
    if x1 == x2 :
        xr = 2 * x1 - xq
        yr = yq

        return xr, yr

    if y1 == y2:
        xr = xq
        yr = 2 * y1 - yq

        return xr, yr

    a = (y2 - y1) / (x2 - x1)
    b = -1
    c = y2 - x2 * (y2 - y1) / (x2 - x1)

    xr = xq - 2 * a * (a * xq + b * yq + c) / (a ** 2 + b ** 2)
    yr = yq - 2 * b * (a * xq + b * yq + c) / (a ** 2 + b ** 2)

    return xr, yr

if __name__ == '__main__':

    x1 = Fraction()
    y1 = Fraction()
    x2 = Fraction()
    y2 = Fraction()
    xq = Fraction()
    yq = Fraction()

    print(symmetric_point(x1, y1, x2, y2, xq, yq))
