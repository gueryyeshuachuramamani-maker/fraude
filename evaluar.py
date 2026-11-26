import json, time
from agente import analizar
from red_bayesiana import p_fraude
from casos_prueba import CASOS

def metricas(pred, y):
    vp = sum(p and l for p, l in zip(pred, y)); fp = sum(p and not l for p, l in zip(pred, y))
    fn = sum((not p) and l for p, l in zip(pred, y)); vn = sum((not p) and (not l) for p, l in zip(pred, y))
    pr = vp / (vp + fp) if vp + fp else 0; rc = vp / (vp + fn) if vp + fn else 0
    f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0
    return dict(VP=vp, FP=fp, FN=fn, VN=vn, precision=pr, recall=rc, f1=f1, exactitud=(vp + vn) / len(y))

res = [analizar(u, t, r) for u, t, r, _ in CASOS]
y = [l for *_, l in CASOS]
# Algoritmo A: red bayesiana, desconocidas omitidas (diseño propuesto), alerta si P>=0.70
A = [r["p_fraude"] >= 0.70 for r in res]
# Algoritmo B: misma red, evidencias desconocidas tratadas como negativas
B = [p_fraude(r["evidencias"], desconocida_como_negativa=True) >= 0.70 for r in res]
# Algoritmo C: regla simple (>=2 evidencias positivas conocidas)
C = [sum(1 for v in r["evidencias"].values() if v is True) >= 2 for r in res]
out = {"A": metricas(A, y), "B": metricas(B, y), "C": metricas(C, y)}

# tiempos (media de 2000 repeticiones por caso)
def t_of(f):
    t0 = time.perf_counter()
    for _ in range(200):
        for u, t, r, _ in CASOS: f(u, t, r)
    return (time.perf_counter() - t0) / (200 * len(CASOS)) * 1e6
out["tiempo_us"] = {"A": t_of(analizar),
                    "C": t_of(lambda u, t, r: (lambda x: sum(1 for v in x["evidencias"].values() if v is True) >= 2)(analizar(u, t, r)))}
# niveles
from collections import Counter
for nombre, lab in (("legitimos", 0), ("fraudes", 1)):
    out["niveles_" + nombre] = dict(Counter(r["nivel"] for r, l in zip(res, y) if l == lab))
out["evid_usadas_media"] = sum(sum(v is not None for v in r["evidencias"].values()) for r in res) / len(res)
out["sin_reputacion"] = sum(r["evidencias"]["R"] is None for r in res)
out["errores"] = [dict(url=r["url"], y=l, p=round(r["p_fraude"], 4), nivel=r["nivel"], ev=r["evidencias"])
                  for r, l in zip(res, y) if (r["p_fraude"] >= .7) != bool(l)]
out["detalle"] = [dict(i=i + 1, url=r["url"], y=l, p=round(r["p_fraude"], 4), nivel=r["nivel"],
                       ev={k: v for k, v in r["evidencias"].items()}) for i, (r, l) in enumerate(zip(res, y))]
json.dump(out, open("resultados.json", "w"), ensure_ascii=False, indent=1)
for k in "ABC": print(k, {a: round(b, 3) for a, b in out[k].items()})
print(out["tiempo_us"], out["niveles_legitimos"], out["niveles_fraudes"], out["evid_usadas_media"], out["sin_reputacion"])
for e in out["errores"]: print(e)
