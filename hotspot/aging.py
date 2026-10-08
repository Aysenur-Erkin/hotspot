import numpy as np

LIFE_H = 180000.

def vRel(hot, upgraded):
    hot = np.asarray(hot, dtype=float)
    if upgraded:
        return np.exp(15000 / (110 + 273) - 15000 / (hot + 273))
    return 2 ** ((hot - 98) / 6)

def lossHrs(v, step):
    return float(np.sum(v) * step / 60)

def yearsLeft(eq, life=LIFE_H):
    if eq <= 0:
        return float("inf")
    return life / eq / 8760
