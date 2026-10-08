from dataclasses import dataclass, field, replace
import numpy as np
from . import profiles, heat, aging
from .params import HOT_LIM, OIL_LIM, BUBBLE

@dataclass
class Out:
    hrs: np.ndarray
    K: np.ndarray
    ta: np.ndarray
    toil: np.ndarray
    thot: np.ndarray
    v: np.ndarray
    tfName: str
    kind: str
    season: str
    peak: float
    upgraded: bool
    dayLoss: float
    eqAge: float
    yrs: float
    warns: list = field(default_factory=list)
    srcLoad: str = "synthetic profile"
    srcAmb: str = "cosine season"

    @property
    def maxHot(self):
        return float(self.thot.max())

    @property
    def whenHot(self):
        h = self.hrs[int(np.argmax(self.thot))]
        return f"{int(h):02d}:{int(round((h % 1) * 60)) % 60:02d}"

    @property
    def maxOil(self):
        return float(self.toil.max())

def run(p, kind="house", peak=1., season="summer", upgraded=None, warmup=3, step=1., load24=None, amb24=None, srcLoad=None, srcAmb=None):
    if upgraded is not None:
        p = replace(p, upgraded=upgraded)
    tot = warmup + 1
    if load24 is not None:
        K = profiles.fromHours(load24, tot, step, peak)
    else:
        K = profiles.loadCurve(kind, peak, tot, step)
    if amb24 is not None:
        ta = profiles.fromHours(amb24, tot, step, 1.)
    else:
        ta = profiles.amb(season, tot, step)
    toil, thot = heat.runTemps(K, ta, p, step)
    n = int(round(24 * 60 / step))
    sl = slice(-n, None)
    K, ta, toil, thot = K[sl], ta[sl], toil[sl], thot[sl]
    hrs = np.arange(n) * step / 60.
    v = aging.vRel(thot, p.upgraded)
    lost = aging.lossHrs(v, step)
    eq = lost / 24.
    o = Out(hrs, K, ta, toil, thot, v, p.name, kind, season, peak, p.upgraded, lost, eq, aging.yearsLeft(eq))
    o.srcLoad = srcLoad or ("hourly override" if load24 is not None else "synthetic " + kind)
    o.srcAmb = srcAmb or ("hourly override" if amb24 is not None else "cosine " + season)
    o.warns = _notes(o)
    return o

def _notes(s):
    w = []
    if s.maxHot > BUBBLE:
        w.append(f"hot {s.maxHot:.1f} over bubble {BUBBLE}")
    elif s.maxHot > HOT_LIM:
        w.append(f"hot {s.maxHot:.1f} over {HOT_LIM}")
    if s.maxOil > OIL_LIM:
        w.append(f"oil {s.maxOil:.1f} over {OIL_LIM}")
    if s.eqAge > 1:
        w.append(f"aging {s.eqAge:.2f}x")
    return w

def sweep(p, kind, season, peaks=None, upgraded=None, load24=None, amb24=None, srcLoad=None, srcAmb=None):
    if peaks is None:
        peaks = np.round(np.arange(.6, 1.55, .1), 2)
    return [run(p, kind, float(k), season, upgraded, load24=load24, amb24=amb24, srcLoad=srcLoad, srcAmb=srcAmb) for k in peaks]

def maxPeak(p, kind="house", season="summer", upgraded=None, lo=.5, hi=2., target=1., n=22, load24=None, amb24=None, srcLoad=None, srcAmb=None):
    lo0, hi0 = lo, hi
    sLo = run(p, kind, lo0, season, upgraded, load24=load24, amb24=amb24, srcLoad=srcLoad, srcAmb=srcAmb)
    sHi = run(p, kind, hi0, season, upgraded, load24=load24, amb24=amb24, srcLoad=srcLoad, srcAmb=srcAmb)
    if sLo.eqAge > target:
        sLo.warns.append(f"K={lo0} already aging {sLo.eqAge:.2f}x > {target}")
        return sLo
    if sHi.eqAge <= target:
        sHi.warns.append(f"K={hi0} still aging {sHi.eqAge:.2f}x <= {target}, cap hit")
        return sHi
    best = lo0
    for _ in range(n):
        mid = .5 * (lo + hi)
        s = run(p, kind, mid, season, upgraded, load24=load24, amb24=amb24, srcLoad=srcLoad, srcAmb=srcAmb)
        if s.eqAge <= target:
            best = mid
            lo = mid
        else:
            hi = mid
    return run(p, kind, best, season, upgraded, load24=load24, amb24=amb24, srcLoad=srcLoad, srcAmb=srcAmb)
