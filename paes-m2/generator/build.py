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
          2: ("clase02", "Logaritmos: concepto, operatoria y propiedades")}
LEVELS = [("principiante", 0), ("avanzado", 1), ("experto", 2)]


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
    wanted = [int(a) for a in argv] or list(CLASES)
    rows = []
    for c in wanted:
        mod, tema = CLASES[c]
        m = importlib.import_module(mod)
        d = DIST / f"clase-{c:02d}"
        d.mkdir(parents=True, exist_ok=True)
        for key, lvl in LEVELS:
            bank = gen_bank(m.BY_SKILL, lvl, 150, seed=c * 1000 + lvl)
            validate(bank, 150)
            html = page(f"Clase {c} · {BRAND['levels'][key]['name']}", key, f"Clase {c}: {tema}", bank, 10)
            (d / f"{key}.html").write_text(html, encoding="utf-8")
            print(f"clase-{c:02d}/{key}.html  {len(html)//1024} KB  banco={len(bank)}")
            rows.append((c, tema, key))
    rows = [(c, CLASES[c][1], k) for c in sorted(CLASES) for k, _ in LEVELS if (DIST / f"clase-{c:02d}" / f"{k}.html").exists()]
    # índice secuencial: clase → nivel
    items = "".join(f'<li>Clase {c}: {t} — ' + " · ".join(f'<a href="clase-{c:02d}/{k}.html">{BRAND["levels"][k]["name"]}</a>'
                    for cc, tt, k in rows if cc == c) + "</li>" for c, t in sorted({(r[0], r[1]) for r in rows}))
    (DIST / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><title>PAES M2 · Evaluaciones</title>'
                                     f'<body style="font-family:Arial;max-width:800px;margin:24px auto;line-height:1.8"><h1>PAES M2 · Evaluaciones</h1><ol>{items}</ol></body>', encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
