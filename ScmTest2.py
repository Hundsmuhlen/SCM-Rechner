import math
import numpy as np
import numpy_ml as npml
from itertools import combinations

def l2metrik(a,b):
    # print(a)
    # print(b)
    return np.linalg.norm(a - b)
    #return npml.utils.distance_metrics.euclidean(a,b)
    #return math.sqrt(a*a + b*b)

def l22metrik(a,b):
    """
    L2² L2quadrat Metrik quadriert die L2 Metrik
    :param a:
    :param b:
    :return:
    """
    return l2metrik(a,b) ** 2

def l1metrik(a,b):
    """
    L1 Metrik oder Manhattan Metrik
    :param a:
    :param b:
    :return:
    """
    return npml.utils.distance_metrics.manhattan(a,b)

def l8metrik(a,b):
    """
    l-unendlich Metrik
    :param a:
    :param b:
    :return:
    """
    return npml.utils.distance_metrics.chebyshev(a,b)


def domKrit(weights, punkte, aj):
    """
    Dominanzkriterium
    :param weights: ohne das Gewicht des aktuellen kandidaten
    :param punkte: ohne den zu betrachtenden punkt
    :return:
    """
    nullvektor = np.array([0,0])
    return l2metrik(sum([wi*((aj-ai)/l2metrik(aj,ai)) for wi,ai in zip(weights,punkte)]),nullvektor)

def delta(k, k1):
    """

    :param k: f(xk)
    :param k1: f(xk+1)-
    :return:
    """
    return ((k-k1)/k)

def l1_zu_l8_transformation(punkte):
    result = []
    matrix = np.array([[1, -1], [1, 1]])
    if type(punkte) is not list:
        punkte = [punkte]

    for punkt in punkte:
        p = np.array(punkt)
        result.append(np.matmul(p, matrix))
    return result

def l8_zu_l1_transformation(punkte:list):
    result = []
    matrix = np.array([[0.5, 0.5], [-0.5, 0.5]])
    if type(punkte) is not list:
        punkte = [punkte]

    for punkt in punkte:
        p = np.array(punkt)
        result.append(np.matmul(p, matrix))
    return result

def l8_center_ungewichtet(punkte):
    all_x = [punkt[0] for punkt in punkte]
    all_y = [punkt[1] for punkt in punkte]
    unten_links = [min(all_x), min(all_y)]
    oben_rechts = [max(all_x), max(all_y)]
    delta_x = abs(oben_rechts[0] - unten_links[0])
    delta_y = abs(oben_rechts[1] - unten_links[1])
    quadrat = lambda dx, dy: dx == dy
    mittelpunkt = [unten_links[0] + delta_x/2, unten_links[1] + delta_y/2]

    return unten_links, oben_rechts, delta_x, delta_y, quadrat(delta_x, delta_y), mittelpunkt

def l8_center_gewichtet_eindimensional(weights, ein_d_punkte):

    delta_ij = lambda wi, ai, wj, aj: float(((wi*wj)/(wi+wj))*abs(aj-ai))
    indizes = [i for i in range(len(ein_d_punkte))]
    combis = [i for i in combinations(indizes, 2)]
    combis_of_actual_points = [[ein_d_punkte[i[0]].copy(), ein_d_punkte[i[1]]].copy() for i in combis]


    delta_list = []
    #delta list hat die gleiche Reihenfolge wie die Liste der möglichen Kombinationen -> deswegen über index auffindbar
    for combi in combis:
        #es sind die kombinierten indizes
        i = combi[0]
        j = combi[1]
        d = delta_ij(weights[i], ein_d_punkte[i], weights[j], ein_d_punkte[j])
        delta_list.append(d)

    print(combis)
    print("--------------")


    delta_max = max(delta_list)
    # print(f"Index of delta max = {delta_list.index(delta_max)}")
    # print(f"Delta Liste= {delta_list}")
    # print(f"Delta Max = {delta_max}")
    combi_of_delta_max = combis[delta_list.index(delta_max)]
    p = combi_of_delta_max[0]
    q = combi_of_delta_max[1]

    opt_punkt = lambda wp,ap,wq,aq: (wp*ap+wq*aq)/(wp+wq)

    x_stern = opt_punkt(weights[p], ein_d_punkte[p], weights[q], ein_d_punkte[q])

    return combis, combis_of_actual_points, delta_list, delta_max, combi_of_delta_max, x_stern

def schwerpunkt(weights,punkte):
    zähler = sum([w*p for w,p in zip(weights, punkte)])
    #print (zähler)
    nenner = sum(weights)
    return zähler/nenner

def entfernung(weights, punkte, center, metrik):
    return sum([w*metrik(p, center) for w, p in zip(weights, punkte)])

def weiszfeld(weights, punkte, xk):
    zähler = sum ([w *(ai/(l2metrik(xk,ai))) for w, ai in zip(weights,punkte)])
    nenner = sum([w/(l2metrik(xk,ai)) for w,ai in zip(weights, punkte)])
    return (zähler/nenner)

def main():
    a = np.array([5,5])
    b = np.array([[1,-1],[1,1]])
    print(a.dot(b))


    punkte = []
    punkte.append(np.array([4,3]))
    punkte.append(np.array([3,18]))
    punkte.append(np.array([16,2]))
    punkte.append(np.array([16,16]))

    weights = [4,5,3,5]
    center = np.array([8.47,7.99])

    print(f"Entfernung : {entfernung(weights, punkte, center)}")

    print(f"Schwerpunkt : {schwerpunkt(weights, punkte)}")
    sp = schwerpunkt(weights, punkte)

    print(f"Weizfeld 1: {weiszfeld(weights,punkte, center)}")
    xk = weiszfeld(weights,punkte, center)
    print(f"{delta(entfernung(weights, punkte, center, l2metrik),entfernung(weights, punkte, xk, l2metrik))}")
    print(f"Entfernung2 : {entfernung(weights, punkte, xk)}")



    # hier startet die Dominanzkriteriumsauslese
    current_number = 0
    weights.pop(current_number)
    aj = punkte.pop(current_number)
    print(f"aj = {aj}")
    print(round(domKrit(weights,punkte, aj),2))


def metriken():
    """
    übersicht über die verschiedenen Metriken
    :return:
    """
    x = np.array([4,0])
    y = np.array([8,9])
    print(l1metrik(x,y))
    print(l2metrik(x,y))
    print(l22metrik(x,y))
    print(l8metrik(x,y))

def SpUndEntfernung():
    punkte = []
    punkte.append(np.array([1,5]))
    punkte.append(np.array([6,0]))
    punkte.append(np.array([7,7]))
    punkte.append(np.array([0,6]))
    punkte.append(np.array([6,4]))


    weights = [7,1,5,1,6]

    print(f"Schwerpunkt : {schwerpunkt(weights, punkte)}")
    center = schwerpunkt(weights, punkte)
    print(f"Entfernung pro Woche: {entfernung(weights,punkte, center, l2metrik())}")



if __name__ == "__main__":
    main()
