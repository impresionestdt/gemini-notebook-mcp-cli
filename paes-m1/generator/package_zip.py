"""Empaqueta dist/ en un ZIP ordenado por clase. Cada archivo se llama «Clase NN - Nivel X Nombre.html»."""
import re, shutil, sys, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build

ROOT = Path(__file__).resolve().parent.parent
dist, out_zip = ROOT / "dist", ROOT / "PAES-M1-por-clases.zip"
LEVEL = {"principiante": "Nivel 1 Principiante", "avanzado": "Nivel 2 Avanzado", "experto": "Nivel 3 Experto"}


def clean(t):
    return re.sub(r'[\\/:*?"<>|]', "-", t).strip()[:70]


with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    for d in sorted(dist.glob("clase-*")):
        n = int(d.name.split("-")[1])
        folder = f"PAES-M1/Clase {n:02d} - {'ENSAYO GENERAL' if n == build.FINAL else clean(build.TITULOS.get(n, ''))}"
        for f in sorted(d.glob("*.html")):
            if f.stem in LEVEL:
                nm = f"Clase {n:02d} - {LEVEL[f.stem]}.html"
            elif f.stem == "mini-ensayo":
                nm = f"Clase {n:02d} - Mini Ensayo.html"
            else:
                nm = f"Clase {n:02d} - Ensayo General.html"
            zf.write(f, f"{folder}/{nm}")
print(out_zip, out_zip.stat().st_size)
