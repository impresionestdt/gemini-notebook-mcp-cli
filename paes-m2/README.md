# PAES M2 · Evaluaciones interactivas (Academia Mirza Cortés)

Cada evaluación es un HTML autocontenido (CSS + JS + banco de preguntas con SVG embebido).

```bash
cd paes-m2/generator
python3 build.py        # regenera todo en ../dist  (o: python3 build.py 1 2)
```

- `brand.json`: colores (provisorios) y color distintivo por nivel.
- `assets/logo.svg`: logo completo (PROVISORIO; reemplazar por el oficial, microscopio + texto).
- `generator/clase01.py`: plantillas paramétricas de la Clase 1.
- `generator/common.py`: regla de alternativas (correcta - distractor más largo <= 16 caracteres) y bancos.
- `generator/template.html`: interfaz del quiz. Revalida la regla de 16 caracteres al cargar,
  elige preguntas al azar balanceando las 5 habilidades y garantiza >= 90 % con imagen.

Entregado: Clase 1 (Principiante / Avanzado / Experto), banco de 150 por nivel, 10 por intento.
