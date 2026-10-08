import numpy as np

def oilRise(K, p):
    return p.dTor * ((1 + K ** 2 * p.R) / (1 + p.R)) ** p.x

def steady(K, ta, p):
    to = ta + oilRise(K, p)
    d1 = p.k21 * p.dThr * K ** p.y
    d2 = (p.k21 - 1) * p.dThr * K ** p.y
    return to, d1, d2

def runTemps(K, ta, p, step=1.):
    n = len(K)
    toA = np.empty(n)
    thA = np.empty(n)
    to, d1, d2 = steady(K[0], ta[0], p)
    for i in range(n):
        toA[i] = to
        thA[i] = to + d1 - d2
        k = K[i]
        a = ta[i]
        tgt = p.dThr * k ** p.y
        to += step / (p.k11 * p.tOil) * (oilRise(k, p) - (to - a))
        d1 += step / (p.k22 * p.tWnd) * (p.k21 * tgt - d1)
        d2 += step / (p.tOil / p.k22) * ((p.k21 - 1) * tgt - d2)
    return toA, thA
