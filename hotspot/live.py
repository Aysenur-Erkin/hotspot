import csv, os, json, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))

# yaklasik ornek, olcum degil
ANK_ORNEK = [23.1, 22.4, 21.8, 21.2, 20.9, 21.4, 23.6, 26.8, 29.7, 32.1, 34.0, 35.4, 36.2, 36.8, 36.5, 35.3, 33.4, 31.2, 29.0, 27.4, 26.1, 25.0, 24.2, 23.6]

def _num(s):
    s = s.strip().replace(".", "").replace(",", ".")
    return float(s)

def _csv_load(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        r = csv.reader(f, delimiter=";")
        next(r)
        for line in r:
            if len(line) < 3:
                continue
            rows.append(_num(line[2]))
    return rows

def epiasCsv():
    files = sorted(os.listdir(DATA)) if os.path.isdir(DATA) else []
    files = [x for x in files if x.lower().endswith(".csv")]
    if not files:
        return None, None
    path = os.path.join(DATA, files[0])
    vals = _csv_load(path)
    if len(vals) < 24:
        return None, None
    vals = vals[:24]
    m = max(vals)
    name = os.path.basename(path)
    return [v / m for v in vals], "EPIAS CSV " + name + " (TR system load, not a feeder)"

def ankaraDay(day="2025-07-28"):
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude=39.9334&longitude=32.8597"
           f"&start_date={day}&end_date={day}"
           "&hourly=temperature_2m&timezone=Europe%2FIstanbul")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "hotspot"})
        with urllib.request.urlopen(req, timeout=12) as r:
            d = json.loads(r.read().decode())
        t = d["hourly"]["temperature_2m"][:24]
        if len(t) == 24 and t[0] is not None:
            return [float(x) for x in t], "Open-Meteo archive Ankara " + day
    except Exception as e:
        print("meteo:", e)
    return list(ANK_ORNEK), "approx sample Ankara summer day (not a measurement)"

def trLoadDay(day="2025-07-28"):
    v, src = epiasCsv()
    if v:
        return v, src
    return None, "no EPIAS CSV in data/"
