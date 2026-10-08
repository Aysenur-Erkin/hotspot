from dataclasses import dataclass

@dataclass
class Xfmr:
    name: str
    dTor: float
    dThr: float
    R: float
    x: float
    y: float
    tOil: float
    tWnd: float
    k11: float
    k21: float
    k22: float
    upgraded: bool = False

READY = {
    "dist_onan": Xfmr("dist ONAN", 55, 23, 5, .8, 1.6, 180, 4, 1, 1, 2),
    "pwr_onan": Xfmr("pwr ONAN", 52, 26, 6, .8, 1.3, 210, 10, .5, 2, 2),
    "pwr_onaf": Xfmr("pwr ONAF", 52, 26, 6, .8, 1.3, 150, 7, .5, 2, 2),
}

HOT_LIM = 120
OIL_LIM = 105
BUBBLE = 140
