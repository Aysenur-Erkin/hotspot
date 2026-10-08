# hotspot

Small IEC 60076-7 hot-spot tool. It takes one day of load and outdoor temperature, steps the oil and winding model, and prints how many hours of paper life that day used.

On a housing feeder in summer, how high can the peak go before the paper ages faster than design? `--max-k` searches that peak factor with bisection.

## Example

```bash
python main.py
```

```
transformer    : dist ONAN
paper          : normal
profile        : house, peak K = 1.00
season         : summer (16-32 C)
load src       : synthetic house
amb src        : cosine summer
max oil        :  73.9 C
max hot        :  95.5 C at 20:06
day loss       :   2.75 hrs
eq aging       :   0.11 x
life           : 179.1 yr   (ref ~20.5)
```

K = 1 means the highest load that day is rated load. On a house curve that peak is only a few evening hours. 0.11x means the day used about 11% of a design day. 179 years is what the 20.5-year reference scale would stretch to if every day looked like this. It is not the tank life. The reference is 180000 h, about 20.5 years (IEEE C57.91).

![Daily load, temperature and aging](docs/day_house_summer.png)

Top: load K and outdoor temperature. Middle: hot-spot, top-oil, ambient, and the IEC cyclic limits. Bottom: relative aging V and hours used. Most of the loss is under the evening peak.

## Commands

```bash
python main.py --xfmr dist_onan --profile house --peak 1.3 --season summer
python main.py --real --max-k
python main.py --real --profile tr --max-k
python main.py --paper upgraded --sweep
python tests.py
```

numpy and matplotlib are enough.

| flag | |
|---|---|
| `--xfmr` | `dist_onan`, `pwr_onan`, `pwr_onaf` |
| `--profile` | `house`, `factory`, `shop`, `flat`, `tr` |
| `--peak` | peak load factor |
| `--season` | `winter`, `spring`, `summer`, `fall` |
| `--paper` | `normal` or `upgraded` |
| `--max-k` | largest K with equivalent aging <= 1 |
| `--sweep` | table of K from 0.6 to 1.5 |
| `--real` | Ankara weather |
| `--profile tr` | EPIAS national load CSV |
| `--out` | plot folder |

## Data

`data/epias_tuketim_2025-07-28.csv` is EPIAS real-time consumption for 28 Jul 2025. It is the whole Turkish system, not one street transformer. Night stays around 64% of the daily peak. A housing feeder drops more at night. That is why `--real --profile tr --max-k` lands near K = 1, and `--real --max-k` (house shape + Ankara air) allows a bit more.

Ankara hourly temperature comes from Open-Meteo when the API answers. If it does not, the code uses an approximate summer day and says so in the printout and on the figure title.

## Model

Top-oil and hot-spot use the IEC 60076-7 difference equations. Oil is slow, the winding is fast, and the hot-spot can overshoot. Normal paper doubles every 6 K, V = 1 at 98 C. Upgraded paper is Arrhenius, V = 1 at 110 C.

`--max-k` bisects K between 0.5 and 2.0. If 0.5 is already too hot, or 2.0 is still cool, it says so instead of reporting a root.
