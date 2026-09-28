# hotspot

A small IEC 60076-7 tool for oil-filled transformers.

Paper around the windings dies with heat. The hottest point in the winding (the hot-spot) sets how fast that happens. This program takes a day of load and outdoor temperature, steps the IEC thermal model, and tells you how much life that day costs.

The question it is built for:

> In summer, on a housing feeder, how high can the peak go before the paper ages faster than design?

`--max-k` answers that with a binary search on peak load factor K.

## What a run looks like

Default command:

```bash
python main.py
```

```
transformer    : dist ONAN
paper          : normal
profile        : house, peak K = 1.00
season         : summer (16…32 C)
load src       : synthetic house
amb src        : cosine summer
max oil        :  73.9 C
max hot        :  95.5 C at 20:06
day loss       :   2.75 hrs
eq aging       :   0.11 x
life           : 179.1 yr   (ref ~20.5)
```

Peak K = 1 means the day's highest load is rated load. On a house curve that peak is only a few evening hours, so most of the day the paper is cool. Equivalent aging 0.11x means that day costs about 11% of a design day. If every day looked like this, the 20.5-year reference scale would stretch a long way. That is expected — it is not a promise that the tank lasts 179 years.

Same day as a plot:

![Daily load, temperature and aging for a distribution ONAN transformer, housing profile, summer, K=1](docs/day_house_summer.png)

Top: load K (blue) and outdoor temperature (green).
Middle: hot-spot, top-oil, ambient, with the IEC cyclic limits.
Bottom: relative aging V and the hours of life used up over the day. Almost all of the loss sits under the evening peak.

## Commands

```bash
python main.py --xfmr dist_onan --profile house --peak 1.3 --season summer
python main.py --real --max-k
python main.py --real --profile tr --max-k
python main.py --paper upgraded --sweep
python tests.py
```

`numpy` and `matplotlib` are enough.

| flag | |
|---|---|
| `--xfmr` | `dist_onan`, `pwr_onan`, `pwr_onaf` |
| `--profile` | `house`, `factory`, `shop`, `flat`, `tr` |
| `--peak` | peak load factor |
| `--season` | `winter`, `spring`, `summer`, `fall` |
| `--paper` | `normal` or `upgraded` |
| `--max-k` | largest K with equivalent aging <= 1 |
| `--sweep` | table of K from 0.6 to 1.5 |
| `--real` | swap in Ankara weather |
| `--profile tr` | use the EPIAS national load CSV |
| `--out` | where plots go |

## Data

`data/epias_tuketim_2025-07-28.csv` is EPIAS real-time consumption for 28 Jul 2025. It is the **whole Turkish system**, not one street transformer. Night stays around 64% of the daily peak, so the machine never really rests. A housing feeder drops much lower at night. That is why `--real --profile tr --max-k` lands near K = 1, while `--real --max-k` (house shape + Ankara air) allows a bit more.

Ankara hourly temperature comes from Open-Meteo when the API answers. If it does not, the code uses an approximate summer day and says so in the printout and on the figure title.

## Model in short

- Top-oil and hot-spot: IEC 60076-7 difference equations (oil is slow, the winding is fast, hot-spot can overshoot).
- Normal paper: aging doubles every 6 K, V = 1 at 98 C.
- Upgraded paper: Arrhenius form, V = 1 at 110 C.
- 180000 h (~20.5 years) is the IEEE C57.91 reference scale, not a nameplate life.

`--max-k` bisects K between 0.5 and 2.0. If 0.5 is already too hot, or 2.0 is still gentle, it says that instead of pretending it found a root.

## Layout

```
main.py          cli
tests.py
docs/            figures used in this readme
data/            EPIAS csv
hotspot/         params, heat, aging, profiles, sim, plots, live
```
