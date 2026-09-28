import numpy as np

SHAPES={
"house":[.45,.40,.38,.37,.37,.40,.50,.60,.62,.60,.58,.58,.60,.58,.57,.58,.65,.78,.92,1,.98,.90,.75,.58],
"factory":[.55,.52,.50,.50,.52,.60,.80,.95,1,1,.98,.97,.85,.95,.98,1,.97,.90,.75,.68,.65,.62,.60,.57],
"shop":[.35,.32,.30,.30,.30,.32,.40,.55,.75,.90,.97,1,1,.98,.97,.95,.92,.88,.80,.70,.60,.50,.42,.38],
"flat":[1.]*24,
}

SEASONS={"winter":(0.,5.),"spring":(12.,7.),"summer":(24.,8.),"fall":(13.,7.)}

def tvec(days,step=1.):
    n=int(round(days*24*60/step))
    return np.arange(n)*step/60.

def loadCurve(kind,peak,days,step=1.):
    raw=np.array(SHAPES[kind],dtype=float)
    raw=raw/raw.max()
    t=tvec(days,step)
    h=t%24
    xs=np.arange(25)
    ys=np.append(raw,raw[0])
    return peak*np.interp(h,xs,ys)

def amb(season,days,step=1.):
    avg,amp=SEASONS[season]
    t=tvec(days,step)
    return avg+amp*np.cos(2*np.pi*(t-15)/24)

def fromHours(hrs,days,step=1.,scale=1.):
    raw=np.array(hrs,dtype=float)
    t=tvec(days,step)
    h=t%24
    xs=np.arange(len(raw)+1)
    ys=np.append(raw,raw[0])
    return scale*np.interp(h,xs,ys)
