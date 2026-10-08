import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hotspot import sim, heat, aging
from hotspot.params import READY

def t1():
    p = READY["dist_onan"]
    n = 60 * 24
    to, th = heat.runTemps(np.ones(n), np.full(n, 20.), p)
    assert abs(to[-1] - 75) < .01
    assert abs(th[-1] - 98) < .01

def t2():
    assert abs(aging.vRel(98, False) - 1) < 1e-9
    assert abs(aging.vRel(110, True) - 1) < 1e-9

def t3():
    v1 = aging.vRel(98, False)
    v2 = aging.vRel(104, False)
    assert abs(v2 / v1 - 2) < 1e-9

def t4():
    p = READY["dist_onan"]
    s1 = sim.go(p, "house", 1, "summer")
    s2 = sim.go(p, "house", 1.3, "summer")
    assert s2.eqAge > s1.eqAge
    assert s2.maxHot > s1.maxHot

def t5():
    p = READY["pwr_onan"]
    n = 60 * 12
    K = np.where(np.arange(n) < 60, .5, 1.2)
    to, th = heat.runTemps(K, np.full(n, 20.), p)
    d = th - to
    assert d.max() > d[-1] + 1

def t6():
    p = READY["dist_onan"]
    s = sim.maxPeak(p, "house", "summer")
    assert abs(s.eqAge - 1) < .02
    assert .5 < s.peak < 2

def t7():
    p = READY["dist_onan"]
    s = sim.maxPeak(p, "house", "summer", lo=1.8, hi=2.0, target=0.01)
    assert any("already aging" in x for x in s.warns)

def t8():
    from hotspot import live
    v, src = live.trLoadDay()
    assert v is not None and len(v) == 24
    assert abs(max(v) - 1) < 1e-9
    assert "EPIAS CSV" in src

if __name__ == "__main__":
    for ad, f in list(globals().items()):
        if ad.startswith("t") and callable(f):
            try:
                f()
                print("ok", ad)
            except Exception as e:
                print("fail", ad, e)
