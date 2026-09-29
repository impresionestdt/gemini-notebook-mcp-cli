# PAES M1 · Evaluaciones interactivas (Academia Mirza Cortés)

Mismo sistema que `paes-m2/`, aplicado a la *Planificación Estratégica PAES M1 (2026-2027)*: 30 semanas, 58 clases (2 por semana).

- `generator/`: plantillas de preguntas (`claseNN.py`, una por clase), figuras (`figs.py`, `geo.py`, `viz.py`), reglas de validación (`common.py`) y `build.py`.
- `dist/clase-NN/`: HTML autocontenidos (CSS, JS, logo y banco de preguntas incrustados).
- Compilar: `cd generator && python3 build.py [clases]` (sin argumentos: todas las disponibles).

## Reglas (idénticas a M2)
- Clases regulares: `principiante.html`, `avanzado.html`, `experto.html`; 10 preguntas al azar de un banco de 150 (≥ 90 % con figura de alto contraste).
- Mini ensayos de cierre de eje (clases 11, 29, 43, 55): un HTML Experto con 20 preguntas de un banco de 250.
- Ensayo General (clase 57): un HTML Experto con 65 preguntas (como la prueba oficial M1) de un banco de 500 con todo el temario.
- 5 alternativas; la correcta no supera por más de 16 caracteres al distractor más largo (se valida al generar y en el navegador).
- 4 habilidades PAES: Resolver problemas, Modelar, Representar y Argumentar (reparto equilibrado).
- Las clases de corrección (12, 30, 44, 56) no llevan quiz.

## Avance
Clases 1 a 18 listas. Siguiente: clase 19.
