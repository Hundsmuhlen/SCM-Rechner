import math
import numpy as np
import numpy_ml as npml

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
    :param weights: ohne das Gewicht des aktuellen kandidaten
    :param punkte: ohne den zu betrachtenden punkt
    :return:
    """
    nullvektor = np.array([0,0])
    return l2metrik(sum([wi*((aj-ai)/l2metrik(aj,ai)) for wi,ai in zip(weights,punkte)]),nullvektor)

def delta(k, k1):
    return ((k-k1)/k)

def schwerpunkt(weights,punkte):
    zähler = sum([w*p for w,p in zip(weights, punkte)])
    #print (zähler)
    nenner = sum(weights)
    return zähler/nenner

def entfernung(weights, punkte, center):
    return sum([w*l2metrik(p,center) for w,p in zip(weights,punkte)])

def weizfeld(weights, punkte, xk):
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

    print(f"Weizfeld 1: {weizfeld(weights,punkte, center)}")
    xk = weizfeld(weights,punkte, center)
    print(f"{delta(entfernung(weights, punkte, center),entfernung(weights, punkte, xk))}")
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
    print(f"Entfernung pro Woche: {entfernung(weights,punkte, center)}")



if __name__ == "__main__":
    main()
