import ScmTest2
import numpy as np
from ScmTest2 import l2metrik


def main():
    # a = np.array([5,10])
    # b = np.array([7,6])
    # c = np.array([4,2])
    # d = np.array([10,4])
    #
    # punkte = [a,b,c,d]
    #
    # mp, radius = mittelpunkt_und_radius(a,d)
    # for punkt in punkte:
    #     print(f"Punkt {punkt} is in radius: {punkt_im_radius(mp, radius,punkt)}")
    #
    # mj, bj = mittelsenkrechte(a,c)
    # print(mj)
    # print(bj)
    # mk, bk = mittelsenkrechte(a,d)
    # print(mk)
    # print(bk)
    # x1,x2 = schnittpunkt_ms(mj,bj,mk,bk)
    # print(f"Schnittpunkt der Mittelsenkrechten: ({x1} , {x2})")
    # print(l2metrik(a, np.array([x1,x2])))
    # print(l2metrik(b, np.array([x1, x2])))

    matrix_mulitplikation()

    # aufg_2()


def online_test3():
    T = np.array([
        [1, -1],
        [1, 1]
    ])

    ost = np.array([15, 20, 19])
    innen = np.array([9, 9, 4])
    süd = np.array([1, 3, 12])

    print(aufg_1(ost[2], innen[2], ost[1], innen[1]))


def aufg_2():
    info = np.array([3, 3])
    masch = np.array([16, 7])
    wiwi = np.array([23, 5])

    print(mittelpunkt(info, masch))
    print(mittelpunkt(info, wiwi))
    print(mittelpunkt(wiwi, masch))

    mi1, bi1 = mittelsenkrechte(masch, wiwi)
    mi2, bi2 = mittelsenkrechte(info, masch)

    x1, x2 = schnittpunkt_ms(mi1, bi1, mi2, bi2)
    print(x1, x2)
    print(mittelpunkt_und_radius(info, wiwi))


def aufg_1(wi, wj, ai, aj):
    return ((wi * wj) / (wi + wj)) * (aj - ai)


def matrix_mulitplikation():
    weights = np.array([
        [9, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 4, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 5]
    ])
    distanzmatrix = np.array([
        [0, 40, 90, 170, 110],
        [40, 0, 50, 210, 90],
        [90, 50, 0, 200, 60],
        [170, 210, 200, 0, 140],
        [110, 90, 60, 140, 0]
    ])
    distanzmatrix3 = np.array([
        [0, 6, 2, 4, 7],
        [6, 0, 3, 6, 3],
        [2, 3, 0, 3, 5],
        [4, 6, 3, 0, 4],
        [7, 3, 5, 4, 0]
    ])
    weights2 = np.array([
        [5, 0, 0, 0],
        [0, 11, 0, 0],
        [0, 0, 5, 0],
        [0, 0, 0, 12],
    ])
    distanzmatrix2 = np.array([
        [0, 0, 5, 6],
        [0, 0, 2, 4],
        [5, 2, 0, 3],
        [6, 4, 3, 0]

    ])
    distanzmatrix2 = np.array([
        [0, 70, 240, 120, 85],
        [70, 0, 274, 83, 15],
        [240, 274, 0, 191, 281],
        [120, 83, 191, 0, 90],
        [85, 15, 281, 90, 0]

    ])
    ergebnis = np.matmul(weights, distanzmatrix)
    print(ergebnis)
    print(ergebnis.sum(axis=0))
    print(np.amax(ergebnis, axis=0))


def punkt_im_radius(mp, radius, punkt):
    if l2metrik(mp, punkt) <= radius:
        return True
    else:
        return False


def mittelpunkt_und_radius(a, b):
    mp = mittelpunkt(a, b)
    radius = l2metrik(mp, a)
    return mp, radius


def mittelpunkt(a, b):
    """

    :param a: np.array von punkt 1
    :param b: np.array von punkt 2
    :return: mittelpunkt als np.array
    """
    x = np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2])
    return x


def mittelsenkrechte(a, b):
    """
    Mittelsenkrechte zwischen den Punkten a und b in der Form:

    y = mi * x + bi
    :param a: np.array oder array
    :param b: np.array oder array
    :return: mi, bi als vorfaktoren
    """
    # print(b[1])
    # print(a[1])
    if a[1] == b[1]:
        raise ValueError("Dividing by 0")
        return None
    bi = (b[0] ** 2 + b[1] ** 2 - a[0] ** 2 - a[1] ** 2) / (2 * (b[1] - a[1]))

    mi = -(a[0] - b[0]) / (a[1] - b[1])
    return mi, bi


def mp_und_radius_drei_auf_gleicher_achse(a, b, c):
    """
    Wenn 3 Punkte auf einer Achse liegen, dann schneiden sich die Mittelsenkrechten nicht!
    :param a:
    :param b:
    :param c:
    :return:
    """
    possible_points = []
    possible_points.append(mittelpunkt_und_radius(a, b))
    possible_points.append(mittelpunkt_und_radius(a, c))
    possible_points.append(mittelpunkt_und_radius(b, c))
    mp, radius = max(possible_points, key=lambda item: item[1])
    return mp, radius

def schnittpunkt_ms(mi1, bi1, mi2, bi2):
    """
    Schnittpunkt von zwei Funktionen, die die Mittelsenkrechten darstellen
    y = mi * x + bi
    :param mi1:
    :param bi1:
    :param mi2:
    :param bi2:
    :return:
    """
    if mi1 == mi2:
        raise ValueError("Can not divide by zero!")
    else:
        x1 = (bi2 - bi1) / (mi1 - mi2)
        x2 = ((mi1 * bi2) - (bi1 * mi2)) / (mi1 - mi2)
        return x1, x2


if __name__ == "__main__":
    main()
