"""Uso: python3 chk.py N  -> verifica bancos (3 niveles), figuras (≥90%), plantillas que fallan y genera hoja de muestra."""
import sys, random, importlib, collections
sys.path.insert(0, '.')
import common
n = int(sys.argv[1])
m = importlib.import_module(f"clase{n:02d}")
for l in range(3):
    try:
        b = common.gen_bank(m.BY_SKILL, l, 150, n * 1000 + l)
        print("nivel", l, "OK", len(b), "figuras", sum(1 for q in b if q["svg"]) / 150)
    except Exception as e:
        print("nivel", l, "ERROR", e)
out = "<body style='display:grid;grid-template-columns:1fr 1fr;gap:8px;width:1200px'>"
for fl in m.BY_SKILL.values():
    for f in fl:
        for l in (0, 2):
            q = None; c = collections.Counter()
            for sd in range(200):
                try:
                    q = f(random.Random(l + sd), l); break
                except Exception as e:
                    c[type(e).__name__ + ":" + str(e)[:40]] += 1
            if q is None:
                print("FALLA", f.__name__, l, dict(c)); continue
            out += f"<div style='border:1px solid #999'><small>{f.__name__} L{l}: {q['q'][:100]} → {q['o'][0]} | {q['o'][1:3]}</small>{q['svg'] or '(sin figura)'}</div>"
open('/tmp/claude-0/sheet.html', 'w').write(out)
