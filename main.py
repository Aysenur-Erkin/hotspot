import argparse, os
from hotspot import plots, sim, live
from hotspot.params import READY
from hotspot.profiles import SEASONS, SHAPES

def parse_args():
    p = argparse.ArgumentParser(description="transformer hot-spot and paper life")
    p.add_argument("--xfmr", choices=READY, default="dist_onan")
    p.add_argument("--profile", choices=list(SHAPES) + ["tr"], default="house")
    p.add_argument("--peak", type=float, default=1.)
    p.add_argument("--season", choices=SEASONS, default="summer")
    p.add_argument("--paper", choices=["normal", "upgraded"], default="normal")
    p.add_argument("--sweep", action="store_true")
    p.add_argument("--max-k", action="store_true")
    p.add_argument("--real", action="store_true",
                   help="Ankara weather + house profile; --profile tr uses EPIAS CSV")
    p.add_argument("--date", default="2025-07-28")
    p.add_argument("--out", default="out")
    p.add_argument("--show", action="store_true")
    return p.parse_args()

def dump(s):
    print("=" * 60)
    print(" HOTSPOT RUN")
    print("=" * 60)
    print(f" transformer    : {s.tfName}")
    paper = "upgraded" if s.upgraded else "normal"
    print(f" paper          : {paper}")
    print(f" profile        : {s.kind}, peak K = {s.peak:.4f}")
    print(f" season         : {s.season} ({s.ta.min():.0f}-{s.ta.max():.0f} C)")
    print(f" load src       : {s.srcLoad}")
    print(f" amb src        : {s.srcAmb}")
    print("-" * 60)
    print(f" max oil        : {s.maxOil:6.1f} C")
    print(f" max hot        : {s.maxHot:6.1f} C (at {s.whenHot})")
    print(f" day loss       : {s.dayLoss:6.2f} hrs")
    print(f" eq aging       : {s.eqAge:6.2f} x")
    y = s.yrs
    ys = "> 200 yr" if y > 200 else f"{y:.1f} yr"
    print(f" life           : {ys}  (ref ~20.5)")
    print("-" * 60)
    if s.warns:
        for u in s.warns:
            print(" !", u)
    else:
        print(" ok")
    print("=" * 60)

def table(rows):
    print(f"{'peak K':>7} | {'hot':>11} | {'aging':>9} | {'life':>10}")
    print("-" * 47)
    for s in rows:
        y = s.yrs
        ys = "> 200 yr" if y > 200 else f"{y:.1f} yr"
        mark = " !" if s.warns else ""
        print(f"{s.peak:7.2f} | {s.maxHot:9.1f}C | {s.eqAge:8.2f}x | {ys:>10}{mark}")

def main():
    a = parse_args()
    p = READY[a.xfmr]
    upgraded = a.paper == "upgraded"
    os.makedirs(a.out, exist_ok=True)
    load24 = amb24 = None
    kind = a.profile
    season = a.season
    srcL = srcA = None
    if a.real or kind == "tr":
        amb24, srcA = live.ankaraDay(a.date)
        season = "ankara"
        if kind == "tr":
            load24, srcL = live.trLoadDay(a.date)
            if load24 is None:
                print("no CSV, falling back to house profile")
                kind = "house"
                srcL = "synthetic house (no CSV)"
            else:
                print("note: TR system load is flat, not a feeder transformer")
        else:
            srcL = "synthetic " + kind + " + Ankara weather"
        print("src load:", srcL)
        print("src amb :", srcA)
    kw = dict(load24=load24, amb24=amb24, srcLoad=srcL, srcAmb=srcA)
    if a.max_k:
        s = sim.maxPeak(p, kind, season, upgraded, **kw)
        print(f"\nmax K with eq aging <= 1 : {s.peak:.4f}  (got {s.eqAge:.4f}x)\n")
        dump(s)
        yol = os.path.join(a.out, f"maxk_{a.xfmr}_{kind}_{season}.png")
        plots.dayPlot(s, yol, a.show)
    elif a.sweep:
        rows = sim.sweep(p, kind, season, upgraded=upgraded, **kw)
        table(rows)
        yol = os.path.join(a.out, f"sweep_{a.xfmr}_{kind}_{season}.png")
        plots.sweepPlot(rows, yol, a.show)
    else:
        s = sim.run(p, kind, a.peak, season, upgraded, **kw)
        dump(s)
        yol = os.path.join(a.out, f"day_{a.xfmr}_{kind}_{season}_K{a.peak:.2f}.png")
        plots.dayPlot(s, yol, a.show)
    print("\nsaved:", yol)

if __name__ == "__main__":
    main()
