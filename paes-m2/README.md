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

Entregado (semanas 1-4 · eje Números):
- Clases 1, 2 y 3: Principiante / Avanzado / Experto, banco de 150 por nivel, 10 por intento (`dist/clase-0N/`).
- Semana 4 · Mini ensayo Números M2 (`dist/clase-04/mini-ensayo.html`): nivel Experto, banco de 250 (50 por habilidad,
  mezcla las plantillas de las clases 1-3 en nivel Experto), 20 por intento.
- Semana 14 · Mini ensayo Álgebra y Funciones M2 (`dist/clase-14/mini-ensayo.html`): igual estructura, con las plantillas de las clases 5-13.
- Semana 22 · Mini ensayo Geometría M2 (`dist/clase-22/mini-ensayo.html`): igual estructura, con las plantillas de las clases 15-21.
- Semana 28 · Mini ensayo Probabilidad y Estadística M2 (`dist/clase-28/mini-ensayo.html`): igual estructura, con las plantillas de las clases 23-27.
Para agregar un mini ensayo o una clase nueva: registrarla en `CLASES` / `MINIS` de `generator/build.py`.
