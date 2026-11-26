"""Interfaz de consola. Uso: python main.py URL [--texto MENSAJE] [--rep reportado|limpio]"""
import argparse
from agente import analizar

NOMBRES = {"D": "Dominio", "R": "Reputación", "U": "Estructura", "C": "Contexto"}


def txt(k, v):
    if v is None:
        return "desconocida (omitida)"
    return {
        "D": ("sospechoso", "no sospechoso"),
        "R": ("reportado", "no reportado"),
        "U": ("anómala", "normal"),
        "C": ("manipulador", "no detectado"),
    }[k][0 if v else 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--texto")
    ap.add_argument("--rep", choices=["reportado", "limpio"])
    a = ap.parse_args()
    r = analizar(a.url, a.texto, {"reportado": True, "limpio": False}.get(a.rep))

    print("=" * 62)
    print(" AGENTE DETECTOR DE ENLACES FRAUDULENTOS")
    print("=" * 62)
    if "error" in r:
        print("Entrada no válida:", r["error"])
        raise SystemExit(2)

    print(f" Enlace : {r['url']}")
    print(" Evidencias:")
    for k, v in r["evidencias"].items():
        print(f"   {k} - {NOMBRES[k]:<11}: {txt(k, v)}")
    if r["senales_texto"]:
        print(f"   Señales en el texto: {', '.join(r['senales_texto'])}")
    print(f" P(Fraude | evidencias) = {r['p_fraude'] * 100:.2f} %")
    print(f" Nivel   : {r['nivel']}")
    print(f" Mensaje : {r['mensaje']}")
    print("=" * 62)


if __name__ == "__main__":
    main()
