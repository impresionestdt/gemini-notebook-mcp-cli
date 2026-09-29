"""Genera los HTML de evaluación PAES M1. Uso: python3 build.py [clase ...]  (por defecto: todas las disponibles)"""
import json, sys, importlib, pathlib
from common import gen_bank, check_lengths, norm, SKILLS
from svgkit import TEXT_ON, contrast

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
LOGO = '<img alt="Academia Mirza Cortés" src="data:image/webp;base64,' + __import__("base64").b64encode((ROOT / "assets" / "logo.webp").read_bytes()).decode() + '">'
TPL = (ROOT / "generator" / "template.html").read_text(encoding="utf-8")
DIST = ROOT / "dist"

# clase -> (módulo, título). Las clases de corrección (12, 30, 44, 56) no llevan quiz.
CLASES = {}
for _n, _t in [
    (1, "Números Enteros: operatoria y prioridades"),
    (2, "Números Enteros: múltiplos, divisores y MCM/MCD"),
    (3, "Números Racionales: operatoria con fracciones, orden y recta numérica"),
    (4, "Números Racionales: decimales, transformación, redondeo y truncamiento"),
    (5, "Razones y proporciones"),
    (6, "Porcentajes I: concepto y cálculo rápido"),
    (7, "Porcentajes II: intereses, aumentos y descuentos"),
    (8, "Potencias de base racional y exponente entero"),
    (9, "Raíces enésimas"),
    (10, "Repaso del eje Números y resolución integrada"),
    (13, "Lenguaje algebraico y evaluación de expresiones"),
    (14, "Operatoria algebraica y reducción"),
    (15, "Productos notables: cuadrado de binomio"),
    (16, "Factorización de expresiones"),
    (17, "Ecuaciones de primer grado I: resolución"),
    (18, "Ecuaciones de primer grado II: planteo"),
    (19, "Sistemas de ecuaciones lineales 2x2 I"),
    (20, "Sistemas de ecuaciones lineales 2x2 II: problemas"),
    (21, "Inecuaciones lineales"),
    (22, "Función: concepto y evaluación"),
    (23, "Función lineal y afín I: gráficas y pendientes"),
    (24, "Función lineal y afín II: modelación"),
    (25, "Función cuadrática I: gráfica y concavidad"),
    (26, "Función cuadrática II: vértice y optimización"),
    (27, "Ecuación cuadrática: intersecciones con el eje X"),
    (28, "Repaso del eje Álgebra y Funciones"),
    (31, "Ángulos y triángulos"),
    (32, "Teorema de Pitágoras"),
    (33, "Figuras planas I: perímetros"),
    (34, "Figuras planas II: áreas"),
    (35, "Cuerpos geométricos: prisma y cilindro"),
    (36, "Plano cartesiano y vectores básicos"),
    (37, "Isometrías: traslación y reflexión"),
    (38, "Isometrías: rotación"),
    (39, "Semejanza de figuras y triángulos"),
    (40, "Proporcionalidad de trazos"),
    (41, "Repaso Geometría I: integración 2D y 3D"),
    (42, "Repaso Geometría II: geometría proporcional"),
    (45, "Tablas de frecuencia"),
    (46, "Gráficos: barras, circulares y líneas"),
    (47, "Medidas de tendencia central (datos no agrupados)"),
    (48, "Medidas de tendencia central (datos agrupados)"),
    (49, "Medidas de posición: cuartiles, percentiles y boxplot"),
    (50, "Probabilidad clásica (regla de Laplace)"),
    (51, "Probabilidad: regla de la suma"),
    (52, "Probabilidad: regla del producto"),
    (53, "Repaso Estadística"),
    (54, "Repaso Probabilidades"),
]:
    CLASES[_n] = (f"clase{_n:02d}", _t)

LEVELS = [("principiante", 0), ("avanzado", 1), ("experto", 2)]
# Mini ensayos de cierre de eje: clase -> (título, clases que integra)
MINIS = {11: ("MINI ENSAYO: Números M1", list(range(1, 11))),
         29: ("MINI ENSAYO: Álgebra y Funciones M1", list(range(13, 29))),
         43: ("MINI ENSAYO: Geometría M1", list(range(31, 43))),
         55: ("MINI ENSAYO: Probabilidad y Estadística M1", list(range(45, 55)))}
FINAL = 57  # Ensayo General: 65 preguntas de un banco de 500 (prueba oficial M1: 65 preguntas)
FINAL_N = 65
TITULOS = {c: t for c, (_, t) in CLASES.items()}
TITULOS.update({c: t for c, (t, _) in MINIS.items()})
TITULOS[FINAL] = "ENSAYO GENERAL PAES M1 (todos los ejes)"


def semana(c):
    return (c + 1) // 2


def available(cl):
    return (pathlib.Path(__file__).parent / f"{CLASES[cl][0]}.py").exists()


def validate(bank, size):
    assert len(bank) == size, len(bank)
    for q in bank:
        assert len(set(q["o"])) == 5
        assert check_lengths(q["o"][0], q["o"][1:]), q
    imgs = sum(1 for q in bank if q["svg"])
    assert imgs / len(bank) >= 0.9, imgs


def page(title, level_key, subtitle, bank, n):
    lv = BRAND["levels"][level_key]
    cfg = json.dumps({"n": n})
    data = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    rep = {"__TITLE__": title, "__PRIMARY__": BRAND["primary"], "__ACCENT__": BRAND["accent"],
           "__LEVEL_COLOR__": lv["color"], "__LEVEL_NAME__": lv["name"], "__SUBTITLE__": subtitle,
           "__LOGO__": LOGO, "__CFG__": cfg, "__BANK__": data}
    out = TPL
    for k, v in rep.items():
        out = out.replace(k, v)
    return out


def merged(classes):
    by = {}
    for cl in classes:
        if not available(cl):
            continue
        for sk, fs in norm(importlib.import_module(CLASES[cl][0]).BY_SKILL).items():
            for f_ in fs:
                if f_ not in by.setdefault(sk, []):
                    by[sk].append(f_)
    return by


def main(argv):
    for fg, bg in TEXT_ON:
        assert contrast(fg, bg) >= 7, (fg, bg)
    for k, v in BRAND["levels"].items():
        assert contrast("#FFFFFF", v["color"]) >= 4.5, k
    wanted = [int(a) for a in argv] or sorted(list(CLASES) + list(MINIS) + [FINAL])
    for c in wanted:
        d = DIST / f"clase-{c:02d}"
        if c in CLASES:
            if not available(c):
                continue
            d.mkdir(parents=True, exist_ok=True)
            m = importlib.import_module(CLASES[c][0])
            for key, lvl in LEVELS:
                bank = gen_bank(m.BY_SKILL, lvl, 150, seed=c * 1000 + lvl)
                validate(bank, 150)
                html = page(f"M1 · Clase {c} · {BRAND['levels'][key]['name']}", key, f"PAES M1 · Clase {c}: {CLASES[c][1]}", bank, 10)
                (d / f"{key}.html").write_text(html, encoding="utf-8")
                print(f"clase-{c:02d}/{key}.html  {len(html)//1024} KB  banco={len(bank)}")
        elif c in MINIS:
            titulo, clases = MINIS[c]
            by = merged(clases)
            if not by or not all(available(cl) for cl in clases):
                continue
            d.mkdir(parents=True, exist_ok=True)
            bank = gen_bank(by, 2, 250, seed=c * 1000 + 7)
            validate(bank, 250)
            html = page(f"M1 · Clase {c} · {titulo}", "mini", f"PAES M1 · Clase {c}: {titulo} (20 preguntas)", bank, 20)
            (d / "mini-ensayo.html").write_text(html, encoding="utf-8")
            print(f"clase-{c:02d}/mini-ensayo.html  {len(html)//1024} KB  banco={len(bank)}")
        elif c == FINAL:
            if not all(available(cl) for cl in CLASES):
                continue
            d.mkdir(parents=True, exist_ok=True)
            per_class = {cl: norm(importlib.import_module(CLASES[cl][0]).BY_SKILL) for cl in CLASES}
            by = {}
            for sk in SKILLS:
                lists = [per_class[cl][sk] for cl in per_class if sk in per_class[cl]]
                seq = []
                for i in range(max(len(x) for x in lists) * len(lists)):
                    seq.append(lists[i % len(lists)][(i // len(lists)) % len(lists[i % len(lists)])])
                by[sk] = seq
            bank = gen_bank(by, 2, 500, seed=c * 1000 + 9)
            validate(bank, 500)
            html = page(f"M1 · Clase {c} · Ensayo General PAES M1", "final", f"PAES M1 · Clase {c}: ENSAYO GENERAL · todos los ejes ({FINAL_N} preguntas)", bank, FINAL_N)
            (d / "ensayo-final.html").write_text(html, encoding="utf-8")
            print(f"clase-{c:02d}/ensayo-final.html  {len(html)//1024} KB  banco={len(bank)}")
    # índice secuencial: clase → nivel o tipo de evaluación
    names = {k: BRAND["levels"][k]["name"] for k, _ in LEVELS}
    names["mini-ensayo"] = BRAND["levels"]["mini"]["name"]
    names["ensayo-final"] = BRAND["levels"]["final"]["name"]
    items = ""
    for c in sorted(TITULOS):
        links = [f'<a href="clase-{c:02d}/{k}.html">{n}</a>' for k, n in names.items() if (DIST / f"clase-{c:02d}" / f"{k}.html").exists()]
        if links:
            items += f"<li>Clase {c} (Semana {semana(c)}): {TITULOS[c]} — " + " · ".join(links) + "</li>"
    (DIST / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>PAES M1 · Evaluaciones</title>'
                                     '<body style="font-family:Arial;max-width:900px;margin:24px auto;line-height:1.8"><h1>PAES M1 · Evaluaciones</h1>'
                                     f'<ol style="list-style:none;padding:0">{items}</ol></body>', encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
