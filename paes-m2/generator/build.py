"""Genera los HTML de evaluación. Uso: python3 build.py [clase ...]  (por defecto: todas las disponibles)"""
import json, sys, importlib, pathlib, itertools
from common import gen_bank, check_lengths
from svgkit import TEXT_ON, contrast

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
LOGO = (ROOT / "assets" / "logo.svg").read_text(encoding="utf-8")
TPL = (ROOT / "generator" / "template.html").read_text(encoding="utf-8")
DIST = ROOT / "dist"

CLASES = {1: ("clase01", "Números Reales e Irracionales: propiedades y racionalización"),
          2: ("clase02", "Logaritmos: concepto, operatoria y propiedades"),
          3: ("clase03", "Porcentajes avanzados e interés compuesto"),
          5: ("clase05", "Ecuación cuadrática avanzada: discriminante y naturaleza de las raíces"),
          6: ("clase06", "Función cuadrática: análisis paramétrico y optimización"),
          7: ("clase07", "Función potencia: gráficas, paridad y traslaciones"),
          8: ("clase08", "Sistemas de inecuaciones lineales"),
          9: ("clase09", "Concepto de función inversa y biyectividad"),
          10: ("clase10", "Función exponencial: modelos de crecimiento y decaimiento"),
          11: ("clase11", "Función logarítmica: gráfica y propiedades")}
LEVELS = [("principiante", 0), ("avanzado", 1), ("experto", 2)]
# Mini ensayos de cierre de unidad: semana -> (título, clases que integra)
MINIS = {4: ("MINI ENSAYO: Números M2", [1, 2, 3])}
TITULOS = {c: t for c, (_, t) in CLASES.items()}
TITULOS.update({w: f"{t} + corrección" for w, (t, _) in MINIS.items()})


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


def main(argv):
    for fg, bg in TEXT_ON:
        assert contrast(fg, bg) >= 7, (fg, bg)
    for k, v in BRAND["levels"].items():
        assert contrast("#FFFFFF", v["color"]) >= 4.5, k
    wanted = [int(a) for a in argv] or list(CLASES) + list(MINIS)
    for c in wanted:
        d = DIST / f"clase-{c:02d}"
        d.mkdir(parents=True, exist_ok=True)
        if c in CLASES:
            m = importlib.import_module(CLASES[c][0])
            for key, lvl in LEVELS:
                bank = gen_bank(m.BY_SKILL, lvl, 150, seed=c * 1000 + lvl)
                validate(bank, 150)
                html = page(f"Clase {c} · {BRAND['levels'][key]['name']}", key, f"Clase {c}: {CLASES[c][1]}", bank, 10)
                (d / f"{key}.html").write_text(html, encoding="utf-8")
                print(f"clase-{c:02d}/{key}.html  {len(html)//1024} KB  banco={len(bank)}")
        else:
            titulo, clases = MINIS[c]
            by = {}
            for cl in clases:
                for sk, fs in importlib.import_module(CLASES[cl][0]).BY_SKILL.items():
                    by.setdefault(sk, []).extend(fs)
            bank = gen_bank(by, 2, 250, seed=c * 1000 + 7)
            validate(bank, 250)
            html = page(f"Semana {c} · {titulo}", "mini", f"Semana {c}: {titulo} (20 preguntas)", bank, 20)
            (d / "mini-ensayo.html").write_text(html, encoding="utf-8")
            print(f"clase-{c:02d}/mini-ensayo.html  {len(html)//1024} KB  banco={len(bank)}")
    # índice secuencial: clase/semana → nivel o tipo de evaluación
    names = {k: BRAND["levels"][k]["name"] for k, _ in LEVELS}
    names["mini-ensayo"] = BRAND["levels"]["mini"]["name"]
    items = ""
    for c in sorted(TITULOS):
        links = [f'<a href="clase-{c:02d}/{k}.html">{n}</a>' for k, n in names.items() if (DIST / f"clase-{c:02d}" / f"{k}.html").exists()]
        if links:
            items += f"<li>Semana {c}: {TITULOS[c]} — " + " · ".join(links) + "</li>"
    (DIST / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>PAES M2 · Evaluaciones</title>'
                                     '<body style="font-family:Arial;max-width:800px;margin:24px auto;line-height:1.8"><h1>PAES M2 · Evaluaciones</h1>'
                                     f'<ol style="list-style:none;padding:0">{items}</ol></body>', encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
